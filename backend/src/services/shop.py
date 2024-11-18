from sqlalchemy import insert, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src import db_tables, exceptions, schemas
from src.services import user


async def all_items(db_session: AsyncSession) -> list[schemas.ShopItem]:
    query = select(db_tables.shop_item)

    items = await db_session.execute(query)

    return [schemas.ShopItem(**item._mapping) for item in items]


async def buy_item(db_session: AsyncSession, user_id: int, item_id: int, price: int):

    inventory_tbl = db_tables.user_inventory
    user_tbl = db_tables.user

    query = (
        pg_insert(inventory_tbl)
        .values(user_id=user_id, item_id=item_id, quantity=1)
        .on_conflict_do_update(
            constraint="inventory_pk", set_=dict(quantity=inventory_tbl.c.quantity + 1)
        )
    )

    await db_session.execute(query)

    query = (
        update(user_tbl)
        .returning(user_tbl.c.coins)
        .where(user_tbl.c.id == user_id)
        .values(coins=user_tbl.c.coins - price)
    )

    new_point = (await db_session.execute(query)).scalar()

    return new_point


async def item_detail(db_session: AsyncSession, item_id: int) -> schemas.ShopItem:
    shop_tbl = db_tables.shop_item

    query = select(shop_tbl).where(shop_tbl.c.id == item_id)

    result = (await db_session.execute(query)).first()

    if result is None:
        raise exceptions.NotFoundException

    return schemas.ShopItem(**result._mapping)
