from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Response, Path

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db

from src.core.hash import get_password_hash, verify_password
from src.core.jwt import (
    create_token_pair,
    decode_access_token,
    add_refresh_token_cookie,
    SUB,
)
from src.exceptions import BadRequestException
from src import schemas


from src.services import user as user_service
from src.services import points as points_service
from src.services import shop as shop_service

import httpx

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
async def register(
    data: schemas.UserRegister,
    response: Response,
    db_session: AsyncSession = Depends(get_db),
):
    user_exist = await user_service.user_exist_by_email(db_session, data.email)

    if user_exist:
        raise HTTPException(status_code=400, detail="Email has already registered")

    hashed_password = get_password_hash(data.password)

    print(hashed_password)

    created_user = await user_service.create_user_by_email(
        db_session, data, hashed_password
    )

    token_pair = create_token_pair(user=created_user)

    add_refresh_token_cookie(response=response, token=token_pair.refresh.token)

    await db_session.commit()

    return {"token": token_pair.access.token, "user_detail": created_user.dict()}


@router.post("/login")
async def login(
    data: schemas.UserLogin,
    response: Response,
    db_session: AsyncSession = Depends(get_db),
):
    if data.google_token is not None:
        # login with google

        async with httpx.AsyncClient() as http_client:
            try:
                user_data = await http_client.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={data.google_token}")
                
                parsed_info = schemas.GoogleCredentalData(**user_data.json())
            except Exception:
                # Invalid token
                raise BadRequestException(detail="Incorrect google token")

        user = await user_service.get_user_by_google_id(db_session, parsed_info.sub)

        print("Google user", user, parsed_info)

        if user is None:
            # a new user
            user = await user_service.create_user_by_google_id(db_session, parsed_info)

    if data.email is not None:
        # login with email
        password = await user_service.user_password_by_email(db_session, data.email)

        if not verify_password(data.password, password):
            raise BadRequestException(detail="Incorrect email or password")

        user = await user_service.user_detail_by_email(db_session, data.email)

    token_pair = create_token_pair(user=user)

    add_refresh_token_cookie(response=response, token=token_pair.refresh.token)

    await db_session.commit()

    return {"token": token_pair.access.token, "user_detail": user.dict(), "avatar": parsed_info.picture}


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db_session: AsyncSession = Depends(get_db),
):
    password = await user_service.user_password_by_email(db_session, form_data.username)

    print(get_password_hash(form_data.password))

    if not verify_password(form_data.password, password):
        raise BadRequestException(detail="Incorrect email or password")

    user = await user_service.user_detail_by_email(db_session, form_data.username)

    token_pair = create_token_pair(user=user)

    add_refresh_token_cookie(response=response, token=token_pair.refresh.token)

    return {"access_token": token_pair.access.token, "token_type": "bearer"}


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db_session: AsyncSession = Depends(get_db),
) -> schemas.UserResponse:
    payload = await decode_access_token(token=token)

    return await user_service.user_by_id(db_session, int(payload[SUB]))

@router.get("/user/{user_id}", response_model=schemas.UserResponse)
async def user_info(
    user: Annotated[schemas.UserResponse, Depends(get_current_user)],
    db_session: AsyncSession = Depends(get_db),
    user_id: int = Path()
) -> schemas.UserResponse:
    
    return await user_service.user_by_id(db_session, user_id)


@router.post("/add_point", response_model=schemas.UserResponse)
async def add_point(
    user: Annotated[schemas.UserResponse, Depends(get_current_user)],
    db_session: AsyncSession = Depends(get_db),
) -> schemas.UserResponse:

    updated_user = await points_service.add_point_for_user(db_session, 300, user.id)

    await db_session.commit()

    return updated_user


@router.get("/leaderboard")
async def leaderboard(
    user: Annotated[schemas.UserResponse, Depends(get_current_user)],
    db_session: AsyncSession = Depends(get_db),
):
    leaderboard = await points_service.leaderboard_of_country(db_session, user.country)

    return {"leaderboard": leaderboard}


@router.get("/shop")
async def shop_items(
    user: Annotated[schemas.UserResponse, Depends(get_current_user)],
    db_session: AsyncSession = Depends(get_db),
):
    items = await shop_service.all_items(db_session)

    return {"items": items}


@router.post("/shop/{item_id}")
async def buy_item(
    user: Annotated[schemas.UserResponse, Depends(get_current_user)],
    db_session: AsyncSession = Depends(get_db),
    item_id: int = Path(),
):
    item_detail = await shop_service.item_detail(db_session, item_id)

    if user.rank.value < item_detail.rank_to_unlock.value:
        raise BadRequestException("User rank is lower than required")

    if user.points < item_detail.price:
        raise BadRequestException("User does not have enough points")

    new_point = await shop_service.buy_item(db_session, user.id, item_id, item_detail.price)

    await db_session.commit()

    return {"points": new_point}
