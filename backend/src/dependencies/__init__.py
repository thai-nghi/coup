from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.dependencies.database import get_db
from src.dependencies.user import get_current_user

UserDependency = Annotated[schemas.UserResponse, Depends(get_current_user)]
DatabaseDependency = Annotated[AsyncSession, Depends(get_db)]
