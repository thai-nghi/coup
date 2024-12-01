import asyncio
import json
import random
from collections import OrderedDict, deque
from typing import Deque

from src.game_server import game_logic
from src.game_server import objects as game_objects
from websockets.exceptions import ConnectionClosedOK
from websockets.server import WebSocketServerProtocol, serve

GAMES: dict[str, game_objects.Game] = {}

PLAYER_GAME: dict[int, game_objects.Game] = {}

FINDING_PLAYERS: OrderedDict[int, game_objects.MatchmakingEntry] = OrderedDict()


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
        ),
        message.player_id: game_objects.Player(
            connection=connection,
            player_id=message.player_id,
            win_piece=[],
            side=second_player_color,
            turn_time=60,
            match_time=60 * 15,
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
    )

    GAMES[game_id] = created_game
    PLAYER_GAME[entry.player_id] = created_game
    PLAYER_GAME[message.player_id] = created_game

    response = game_objects.GameResponse(game=created_game)

    try:
        game_json = response.model_dump_json(
            exclude={
                "game": {
                    "players": {
                        entry.player_id: {"connection"},
                        message.player_id: {"connection"},
                    }
                }
            }
        )
        await connection.send(game_json)
        await entry.connection.send(game_json)
    finally:
        pass


async def play_game(connection: WebSocketServerProtocol, player_id: int):
    async for raw_message in connection:
        pass

    game = PLAYER_GAME.pop(player_id, None)
    FINDING_PLAYERS.pop(player_id, None)

    if game is not None:
        GAMES.pop(game.id, None)


async def websocket_handler(connection: WebSocketServerProtocol):
    print("Connection established")
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
                        connection=connection, player_id=player_id
                    )
                    await play_game(connection, player_id)
    except ConnectionClosedOK:
        game = PLAYER_GAME.pop(player_id, None)
        FINDING_PLAYERS.pop(player_id, None)

        if game is not None:
            GAMES.pop(game.id, None)


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
