from src.dependencies.database import get_db

from src.dependencies.user import get_current_user

from typing import Annotated

from src import schemas

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from fastapi import Depends

UserDependency = Annotated[schemas.UserResponse, Depends(get_current_user)]
DatabaseDependency = Annotated[AsyncSession, Depends(get_db)]