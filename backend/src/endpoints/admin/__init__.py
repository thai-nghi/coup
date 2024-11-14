from fastapi import APIRouter
from src.endpoints.admin.game import router as game_router

router = APIRouter(prefix="/admin")

router.include_router(game_router)
