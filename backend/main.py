from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from src.endpoints.admin import router as admin_router
from src.endpoints.auth import router as auth_router
from src.endpoints.game import router as game_router
from src.endpoints.metadata import router as metadata_router
from src.endpoints.shop import router as shop_router
from src.endpoints.user import router as user_router
from src.endpoints.webhook import router as webhook_router

app = FastAPI(default_response_class=ORJSONResponse)

origins = ["http://localhost", "http://localhost:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (
    auth_router,
    shop_router,
    user_router,
    game_router,
    admin_router,
    webhook_router,
    metadata_router,
):
    app.include_router(router)
