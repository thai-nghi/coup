from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from fastapi.middleware.cors import CORSMiddleware

from src.endpoints.auth import router as auth_router
from src.endpoints.shop import router as shop_router
from src.endpoints.user import router as user_router
from src.endpoints.game import router as game_router

app = FastAPI(default_response_class=ORJSONResponse)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (auth_router, shop_router, user_router, game_router):
    app.include_router(router)
