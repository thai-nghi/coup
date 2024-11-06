import pytest
from src.core.config import settings
from src.dependencies.database import create_engine_from_setting
from alembic import command, config
from main import app
import pytest_asyncio
from pytest_asyncio import is_async_test
import httpx

from sqlalchemy import text

def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest_asyncio.fixture(loop_scope="function", scope="function")
def test_settings():
    return settings


@pytest_asyncio.fixture(loop_scope="session", scope="function")
async def test_db(test_settings):

    cfg = config.Config("./alembic.ini")
    engine = create_engine_from_setting(test_settings)

    def run_upgrade(connection):
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, "head")

    def run_downgrade(connection):
        cfg.attributes["connection"] = connection
        command.downgrade(cfg, "base")

    async with engine.begin() as connection:
        await connection.run_sync(run_upgrade)

        with open("./sql_scripts/countries.sql") as file:
            query = text(file.read())

        await connection.execute(query)

    yield

    async with engine.begin() as connection:
        await connection.run_sync(run_downgrade)


@pytest_asyncio.fixture(loop_scope="session", scope="function")
def test_app(test_db):
    return app


@pytest_asyncio.fixture(loop_scope="session", scope="function")
async def authenticated_client(test_app):
    new_user_data = {
        "email": "test@gmail.com",
        "display_name": "Test Full name",
        "country_id": "10",
    }
    async with httpx.AsyncClient(app=test_app, base_url="http://coup.test") as client:
        result = await client.post(
            "/auth/register",
            json={**new_user_data, "password": "123", "confirm_password": "123"},
        )
        assert result.status_code == 200

        data = result.json()
    
    async with httpx.AsyncClient(app=test_app, base_url="http://coup.test", headers={
        "Authorization": f"Bearer {data['token']}"
    }, follow_redirects=True) as client:
        yield client
