from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)


from ..core import config


def create_engine_from_setting(setting: config.Settings):
    PG_URL = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        username=setting.POSTGRES_USER,
        password=setting.POSTGRES_PASSWORD,
        host=setting.POSTGRES_HOST,
        port=setting.DB_PORT,
        path=f"{setting.POSTGRES_DB}",
    )

    return create_async_engine(str(PG_URL) + "?prepared_statement_cache_size=0", future=True, echo=True)


engine = create_engine_from_setting(config.settings)


SessionFactory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        await db.close()
