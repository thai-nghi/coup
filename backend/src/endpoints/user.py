from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src import schemas
from src.core.config import settings
from src.dependencies import DatabaseDependency
from src.dependencies.user import get_current_user
from src.exceptions import AuthFailedException, BadRequestException
from src.services import user

router = APIRouter(
    prefix="/user", dependencies=[Depends(get_current_user)], tags=["user"]
)


@router.get("/", response_model=schemas.UserResponse)
async def user_profile(
    user: Annotated[schemas.UserResponse, Depends(get_current_user)]
) -> schemas.UserResponse:

    return user
