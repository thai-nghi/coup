from src import db_tables
from src import schemas
from src import exceptions

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from sqlalchemy import select, insert


async def record_match_result(db_session: AsyncSession, match_data: schemas.MatchResultIn):
    match_tbl = db_tables.matches
    player_match_tbl = db_tables.player_matches
    elo_change_tbl = db_tables.elo_change
    coin_change_tbl = db_tables.coin_change

    query = insert(match_tbl).values(replay=match_data.match_replay, type=match_data.type)

    new_match_id = (await db_session.execute(query)).inserted_primary_key[0]

    for player_result in match_data.player_result:
        player_id = player_result.player_id
        query = insert(player_match_tbl).values(match_id = new_match_id, player_id=player_id, result=player_result.result)

        await db_session.execute(query)

        query = insert(elo_change_tbl).values(player_id=player_id, elo_change=player_result.elo_change, match_id = new_match_id)
        await db_session.execute(query)

        query = insert(coin_change_tbl).values(player_id=player_id, coin_change=player_result.coin_change, event_id=new_match_id)

