import asyncio
import json

from pydantic import PostgresDsn
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src import db_tables
from src.core.config import settings

PG_URL = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.DB_PORT,
    path=settings.POSTGRES_DB,
)


engine = create_async_engine(
    str(PG_URL) + "?prepared_statement_cache_size=0", future=True, echo=True
)


async def main():
    with open("./data_files/shop.json") as file:
        items = json.load(file)

    async with engine.begin() as connection:
        await connection.execute(insert(db_tables.shop_item).values(items))


asyncio.run(main())
