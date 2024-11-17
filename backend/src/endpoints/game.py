import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src import schemas
from src.core.config import settings
from src.dependencies import DatabaseDependency, UserDependency
from src.dependencies.user import get_current_user
from src.exceptions import AuthFailedException, BadRequestException
from src.schemas import response
from src.services import game

router = APIRouter(prefix="/game", dependencies=[Depends(get_current_user)])


@router.post("/play")
async def find_match():
    """ """
    pass


@router.post("/lobby")
async def create_lobby():
    """ """
    pass


@router.post("/lobby/{lobby_id}")
async def join_lobby():
    """ """
    pass


@router.get("/watch/{match_id}")
async def watch_game():
    """ """
    pass


@router.get("/lobby", response_model=list[schemas.NewMatchData])
async def list_lobbies(
    page: Annotated[int, Query()] = 1,
    page_size: Annotated[int, Query()] = 20,
) -> schemas.NewMatchData:
    return await game.live_match_list(page=page, page_size=page_size)


@router.get("/history", response_model=response.MatchHistory)
async def match_history(
    user_data: UserDependency,
    db_session: DatabaseDependency,
    page: Annotated[int, Query()] = 1,
) -> response.MatchHistory:

    return await game.user_match_history(db_session, user_data.id, page)


@router.get("/history_summary", response_model=response.MatchHistorySummary)
async def match_history_summary(
    user_data: UserDependency,
    db_session: DatabaseDependency,
) -> response.MatchHistorySummary:
    return await game.user_match_history_summary(db_session, user_data.id)
