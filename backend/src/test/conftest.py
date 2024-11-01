import pytest
from src.core.config import settings
from src.dependencies.database import create_engine_from_setting
from alembic import command, config
from main import app

cfg = config.Config("/path/to/yourapp/alembic.ini")


@pytest.fixture
def test_settings():
    return settings

@pytest.fixture
async def test_db(test_settings):


    cfg = config.Config("./alembic.ini")
    engine = create_engine_from_setting(test_settings)

    def run_upgrade(connection):
        cfg.attributes['connection'] = connection
        command.upgrade(cfg, "head")

    def run_downgrade(connection):
        cfg.attributes['connection'] = connection
        command.downgrade(cfg, "base")

    async with engine.begin() as connection:
        await connection.run_sync(run_upgrade)

    print("Finish running upgrade")

    yield 1
    
    async with engine.begin() as connection:
        await connection.run_sync(run_downgrade)

@pytest.fixture
def test_app(test_db):
    return app