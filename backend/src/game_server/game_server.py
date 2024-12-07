import asyncio
import json
import random
from collections import OrderedDict

import httpx
from src.game_server import game_logic
from src.game_server import objects as game_objects
from src.game_server.game_server_setting import GAME_SERVER_SETTINGS
from src.schemas import (
    MatchResult,
    MatchResultIn,
    MatchType,
    NewMatchData,
    PlayerResult,
    PlayerSummary,
)
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from websockets.server import WebSocketServerProtocol, serve

GAMES: dict[str, game_objects.Game] = {}

PLAYER_GAME: dict[int, game_objects.Game] = {}

FINDING_PLAYERS: OrderedDict[int, game_objects.MatchmakingEntry] = OrderedDict()


async def report_match_result(game: game_objects.Game, winner: int):
    print(f"Report match result, winner: {winner}")

    winner_result = PlayerResult(
        player_id=winner, elo_change=15, result=MatchResult.WIN, coin_change=100
    )
    loser = game.opponent_id[winner]

    loser_result = PlayerResult(
        player_id=loser, elo_change=-10, result=MatchResult.LOSE, coin_change=20
    )

    async with httpx.AsyncClient(
        base_url=GAME_SERVER_SETTINGS.API_HOST,
        headers={"Authorization": f"Bearer {GAME_SERVER_SETTINGS.GAME_SERVER_ACCESS}"},
    ) as client:

        data = MatchResultIn(
            match_id=game.id,
            match_replay="",
            move_first_player=game.move_first_player,
            player_result=[winner_result, loser_result],
            type=game.match_type,
        )

        response = await client.post("/game/result", json=data.model_dump(mode="json"))
        print(response.text)

    return {
        winner_result.player_id: winner_result,
        loser_result.player_id: loser_result,
    }


async def send_message(
    connection: WebSocketServerProtocol,
    message: game_objects.BaseResposne,
    exclude=None,
) -> bool:
    try:
        await connection.send(message.model_dump_json(exclude=exclude))
    except (ConnectionClosedOK, ConnectionClosedError) as err:
        print(f"Error when sending: {str(err)}")
        return False
    return True


async def clean_disconnect(player_id: int):
    game = PLAYER_GAME.pop(player_id, None)
    FINDING_PLAYERS.pop(player_id, None)

    if game is not None:
        GAMES.pop(game.id, None)

        opp_id = game.opponent_id[player_id]

        if not game.game_end:

            if game.players_ready >= 2:
                # game started, who disconnect loses or who being called this function first loses
                player_results = await report_match_result(game, opp_id)
                game.game_end = True

                for player in game.players.values():
                    await send_message(
                        player.connection,
                        game_objects.MatchResultResponse(
                            result=player_results[player.player_id].result,
                            elo_change=player_results[player.player_id].elo_change,
                            coin_change=player_results[player.player_id].coin_change,
                        ),
                    )
            else:
                response = game_objects.MatchCancelResponse()
                await send_message(
                    game.players[opp_id].connection,
                    response,
                )
        PLAYER_GAME.pop(opp_id, None)


async def report_live_match(game: game_objects.Game):

    async with httpx.AsyncClient(
        base_url=GAME_SERVER_SETTINGS.API_HOST,
        headers={"Authorization": f"Bearer {GAME_SERVER_SETTINGS.GAME_SERVER_ACCESS}"},
    ) as client:
        data = NewMatchData(
            match_id=game.id,
            player_data=[
                PlayerSummary(
                    player_id=player.player_id,
                    display_name=player.display_name,
                    elo=player.elo,
                )
                for player in game.players.values()
            ],
        )

        response = await client.post(
            "/game/new_game", json=data.model_dump(mode="json")
        )
        print(response.text)


async def start_game(
    entry: game_objects.MatchmakingEntry,
    message: game_objects.FindMatchMessage,
    connection: WebSocketServerProtocol,
):
    # decide move first
    # init player
    first_player_color = (
        game_objects.PieceColor.WHITE
        if random.randint(1, 100) <= 50
        else game_objects.PieceColor.BLACK
    )

    if first_player_color == game_objects.PieceColor.WHITE:
        second_player_color = game_objects.PieceColor.BLACK
        move_first_player = entry.player_id
    else:
        second_player_color = game_objects.PieceColor.WHITE
        move_first_player = message.player_id

    players = {
        entry.player_id: game_objects.Player(
            connection=entry.connection,
            player_id=entry.player_id,
            win_piece=[],
            side=first_player_color,
            turn_time=60,
            match_time=60 * 15,
            elo=entry.elo,
            display_name=entry.display_name,
        ),
        message.player_id: game_objects.Player(
            connection=connection,
            player_id=message.player_id,
            win_piece=[],
            side=second_player_color,
            turn_time=60,
            match_time=60 * 15,
            elo=message.elo,
            display_name=message.display_name,
        ),
    }
    # init board
    game_board = game_logic.init_game_board()

    game_id = f"{entry.player_id}_{message.player_id}"

    created_game = game_objects.Game(
        chess_board=game_board,
        players=players,
        current_turn_id=move_first_player,
        id=game_id,
        opponent_id={
            entry.player_id: message.player_id,
            message.player_id: entry.player_id,
        },
        match_type=MatchType.RANKED,
        move_first_player=move_first_player,
    )

    GAMES[game_id] = created_game
    PLAYER_GAME[entry.player_id] = created_game
    PLAYER_GAME[message.player_id] = created_game

    response = game_objects.RequestReadyResponse()

    first_success = await send_message(connection, response)

    second_success = await send_message(entry.connection, response)

    if first_success and second_success:
        await report_live_match(created_game)
        await wait_confirm(connection, message.player_id)
        return

    response = game_objects.MatchCancelResponse()

    if first_success:
        await send_message(connection, response)
        await clean_disconnect(message.player_id)

    if second_success:
        await send_message(entry.connection, response)
        await clean_disconnect(entry.player_id)


async def play_game(connection: WebSocketServerProtocol, player_id: int):
    async for raw_message in connection:

        message = game_objects.message_type_adapter.validate_python(
            json.loads(raw_message)
        )

        if message.message_id == game_objects.MessageId.CANCEL:
            break

        if message.message_id == game_objects.MessageId.MOVE:
            game = PLAYER_GAME.get(player_id)

            if game is None:
                break

            if game.current_turn_id != player_id:
                continue

            if not game_logic.validate_move(
                message.start_addr,
                message.dest_addr,
                game.chess_board,
                game.players[player_id].side,
            ):
                continue

            game_logic.move_piece(
                message.start_addr, message.dest_addr, game.chess_board
            )

            if game_logic.is_check_mate(
                game.players[game.opponent_id[player_id]].side,
                game.chess_board,
            ):
                # end game
                print(f"Check mate found, player who who check mate {player_id}")
                await clean_disconnect(game.opponent_id[player_id])
                break

            game.current_turn_id = game.opponent_id[player_id]
            response = game_objects.GameResponse(game=game)

            for player in game.players.values():
                send_success = await send_message(
                    player.connection,
                    response,
                    {
                        "game": {
                            "players": {
                                player_id: {"connection"},
                                game.opponent_id[player_id]: {"connection"},
                            }
                        }
                    },
                )

                if not send_success:
                    await clean_disconnect(game.opponent_id[player_id])
                    break

    print(f"Player {player_id} disconnect during play game")

    await clean_disconnect(player_id)


async def wait_confirm(connection: WebSocketServerProtocol, player_id: int):
    async for raw_message in connection:
        message = game_objects.message_type_adapter.validate_python(
            json.loads(raw_message)
        )

        if message.message_id == game_objects.MessageId.CANCEL:
            break

        if message.message_id == game_objects.MessageId.READY:
            game = PLAYER_GAME.get(player_id)

            if game is None:
                continue

            send_success = True

            if not game.players[player_id].ready:
                game.players_ready = game.players_ready + 1
                game.players[player_id].ready = True

                if game.players_ready == 2:
                    response = game_objects.GameResponse(game=game)

                    for player in game.players.values():
                        send_success = await send_message(
                            player.connection,
                            response,
                            {
                                "game": {
                                    "players": {
                                        player_id: {"connection"},
                                        game.opponent_id[player_id]: {"connection"},
                                    }
                                }
                            },
                        )

                        if not send_success:
                            await clean_disconnect(player.player_id)
                            break

                if send_success:
                    await play_game(connection, player_id)
    print(f"Player {player_id} disconnect during confirm")

    await clean_disconnect(player_id)


async def websocket_handler(connection: WebSocketServerProtocol):
    player_id = None

    try:

        raw_message = await connection.recv()

        message = game_objects.message_type_adapter.validate_python(
            json.loads(raw_message)
        )

        print(
            f"Connecting player: {message.player_id}, current queue {len(FINDING_PLAYERS)}, current match {len(GAMES)}"
        )

        if message.message_id == game_objects.MessageId.FIND_MATCH:
            player_id = message.player_id
            if player_id not in FINDING_PLAYERS:
                if FINDING_PLAYERS:
                    entry = FINDING_PLAYERS.popitem(last=True)
                    await start_game(entry[1], message, connection)
                else:
                    FINDING_PLAYERS[player_id] = game_objects.MatchmakingEntry(
                        connection=connection,
                        player_id=player_id,
                        elo=message.elo,
                        display_name=message.display_name,
                    )
                    await wait_confirm(connection, player_id)

    except (ConnectionClosedOK, ConnectionClosedError):
        await clean_disconnect(player_id)


async def websocket_server():
    print("Init webserver")
    async with serve(websocket_handler, "192.168.31.115", 4000):
        await asyncio.get_running_loop().create_future()


async def game_update():
    print("start game update")
    pass


async def main():
    await asyncio.gather(websocket_server(), game_update())


if __name__ == "main":
    exit()

asyncio.run(main())
