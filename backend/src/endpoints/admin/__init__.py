from fastapi import APIRouter, Depends
from src.dependencies.user import get_current_user
from src.endpoints.webhook.game import router as game_router

router = APIRouter(prefix="/admin", dependencies=[Depends(get_current_user)])
