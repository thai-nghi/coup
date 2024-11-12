from typing import Annotated
from fastapi import APIRouter, Depends, Path, Request

from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import DatabaseDependency
from src.dependencies.user import get_current_user

from src.exceptions import BadRequestException, AuthFailedException
from src import schemas
from src.core.config import settings
from src.services import game

router = APIRouter(prefix="/game", dependencies=[Depends(get_current_user)])

@router.post("/play")
async def find_match():
    """
    """
    pass

@router.post("/lobby")
async def create_lobby():
    """
    """
    pass

@router.post("/lobby/{lobby_id}")
async def join_lobby():
    """
    """
    pass


@router.get("/watch/{match_id}")
async def watch_game():
    """
    """
    pass

@router.get("/lobby")
async def list_lobbies():
    """
    """
    pass

@router.post("/result")
async def submit_result(
    request: Request,
    match_data: schemas.MatchResultIn,
    db_session: DatabaseDependency
):
    if request.headers.get("Authorization") != f"Bearer {settings.GAME_SERVER_ACCESS}":
        raise AuthFailedException("Not authorized for this endpoint")
    
    await game.record_match_result(db_session, match_data)

    db_session.commit()

    