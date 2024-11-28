from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from src import schemas
from src.dependencies.database import get_db
from src.dependencies.user import get_current_user
from src.exceptions import BadRequestException
from src.schemas import response
from src.services import shop as shop_service

router = APIRouter(
    prefix="/shop", dependencies=[Depends(get_current_user)], tags=["shop"]
)


@router.get("/", response_model=response.ShopResponse)
async def shop_items(
    db_session: AsyncSession = Depends(get_db),
):
    return await shop_service.all_items(db_session)


@router.post("/{item_id}")
async def buy_item(
    user: Annotated[schemas.UserResponse, Depends(get_current_user)],
    db_session: AsyncSession = Depends(get_db),
    item_id: int = Path(),
):
    item_detail = await shop_service.item_detail(db_session, item_id)

    if user.coins < item_detail.price:
        raise BadRequestException("User does not have enough coins")

    new_point = await shop_service.buy_item(
        db_session, user.id, item_id, item_detail.price
    )

    await db_session.commit()

    return {"points": new_point}
