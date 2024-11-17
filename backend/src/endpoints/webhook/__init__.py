from fastapi import APIRouter
from src.endpoints.webhook.game import router as game_router

router = APIRouter(prefix="/webhooks")

router.include_router(game_router)
