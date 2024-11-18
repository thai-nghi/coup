from collections import OrderedDict

from sqlalchemy import and_, cte, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src import db_tables, exceptions, schemas
from src.schemas import response

live_matches = OrderedDict()


async def record_match_result(
    db_session: AsyncSession, match_data: schemas.MatchResultIn
):
    live_matches.pop(match_data.match_id)

    match_tbl = db_tables.matches
    player_match_tbl = db_tables.player_matches
    elo_change_tbl = db_tables.elo_change
    coin_change_tbl = db_tables.coin_change
    user_tbl = db_tables.user

    query = insert(match_tbl).values(
        replay=match_data.match_replay, type=match_data.type
    )

    new_match_id = (await db_session.execute(query)).inserted_primary_key[0]

    for player_result in match_data.player_result:
        player_id = player_result.player_id
        query = insert(player_match_tbl).values(
            match_id=new_match_id, player_id=player_id, result=player_result.result
        )

        await db_session.execute(query)

        query = insert(elo_change_tbl).values(
            player_id=player_id,
            elo_change=player_result.elo_change,
            match_id=new_match_id,
        )
        await db_session.execute(query)

        query = insert(coin_change_tbl).values(
            player_id=player_id,
            coin_change=player_result.coin_change,
            event_id=new_match_id,
            event_type=schemas.CoinChangeEventType.MATCH,
        )

        await db_session.execute(query)

        query = (
            update(user_tbl)
            .values(
                elo=user_tbl.c.elo + player_result.elo_change,
                coins=user_tbl.c.coins + player_result.coin_change,
            )
            .where(user_tbl.c.id == player_id)
        )

        await db_session.execute(query)


async def user_match_history(
    db_session: AsyncSession, user_id: int, page: int = 1, page_size: int = 20
) -> response.MatchHistory:
    match_tbl = db_tables.matches
    player_match_tbl = db_tables.player_matches
    elo_change_tbl = db_tables.elo_change
    coin_change_tbl = db_tables.coin_change

    coin_change_subquery = (
        select(
            coin_change_tbl.c.player_id,
            coin_change_tbl.c.coin_change,
            coin_change_tbl.c.event_id,
        )
        .where(coin_change_tbl.c.player_id == user_id)
        .where(coin_change_tbl.c.event_type == schemas.CoinChangeEventType.MATCH)
        .subquery()
    )

    query = (
        select(
            player_match_tbl.c.player_id,
            player_match_tbl.c.match_id,
            player_match_tbl.c.result,
            match_tbl.c.match_time,
            match_tbl.c.type,
            elo_change_tbl.c.elo_change,
            coin_change_subquery.c.coin_change,
        )
        .select_from(
            player_match_tbl.join(
                match_tbl, player_match_tbl.c.match_id == match_tbl.c.id
            )
            .join(
                elo_change_tbl,
                and_(
                    player_match_tbl.c.match_id == elo_change_tbl.c.match_id,
                    player_match_tbl.c.player_id == elo_change_tbl.c.player_id,
                ),
            )
            .join(
                coin_change_subquery,
                and_(
                    player_match_tbl.c.match_id == coin_change_subquery.c.event_id,
                ),
            )
        )
        .where(player_match_tbl.c.player_id == user_id)
        .order_by(match_tbl.c.match_time.desc())
        .limit(page_size)
        .offset((page - 1) * page_size)
    )

    match_results = await db_session.execute(query)

    return response.MatchHistory(
        page_size=page_size,
        page=page,
        matches=[schemas.MatchHistoryEntry(**row._mapping) for row in match_results],
    )


async def user_match_history_summary(
    db_session: AsyncSession, user_id: int
) -> response.MatchHistorySummary:
    player_match_tbl = db_tables.player_matches

    query = (
        select(
            player_match_tbl.c.player_id,
            func.count()
            .filter(player_match_tbl.c.result == schemas.MatchResult.WIN)
            .label("win"),
            func.count()
            .filter(player_match_tbl.c.result == schemas.MatchResult.LOSE)
            .label("loss"),
        )
        .where(player_match_tbl.c.player_id == user_id)
        .group_by(player_match_tbl.c.player_id)
    )

    summary = (await db_session.execute(query)).first()

    if summary is None:
        return response.MatchHistorySummary(win=0, loss=0, total_match=0)

    return response.MatchHistorySummary(
        win=summary.win, loss=summary.loss, total_match=summary.win + summary.loss
    )


async def record_live_match(
    match_data: schemas.NewMatchData,
):
    live_matches[match_data.match_id] = match_data


async def live_match_list(
    page: int = 1, page_size: int = 20
) -> list[schemas.NewMatchData]:
    start_index = (page - 1) * page_size

    return list(live_matches.values())[start_index : start_index + page_size]
