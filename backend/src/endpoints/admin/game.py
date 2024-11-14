from fastapi import APIRouter, Depends, Path, Query, Request
from src import schemas
from src.core.config import settings
from src.dependencies import DatabaseDependency
from src.exceptions import AuthFailedException, BadRequestException
from src.schemas import response
from src.services import game

router = APIRouter(prefix="/game")


@router.post("/result")
async def submit_result(
    request: Request, match_data: schemas.MatchResultIn, db_session: DatabaseDependency
):
    if request.headers.get("Authorization") != f"Bearer {settings.GAME_SERVER_ACCESS}":
        raise AuthFailedException("Not authorized for this endpoint")

    await game.record_match_result(db_session, match_data)

    await db_session.commit()
