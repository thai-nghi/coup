import pytest
from src.core.config import settings
from src.dependencies.database import create_engine_from_setting
from alembic import command, config
from main import app
import pytest_asyncio
from pytest_asyncio import is_async_test
import httpx
import json
from src.core.hash import get_password_hash, verify_password
from src import db_tables
from sqlalchemy import text, insert


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

        with open("./data_files/countries.sql") as file:
            query = text(file.read())

        await connection.execute(query)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(run_downgrade)


@pytest_asyncio.fixture(loop_scope="session", scope="function")
async def user_factory(test_db):
    with open("./data_files/users.json") as file:
        users = json.load(file)

    insert_users = [
        {**user, "password": get_password_hash(user["password"])} for user in users
    ]

    async with test_db.begin() as connection:
        await connection.execute(insert(db_tables.user).values(insert_users))

    return {user["display_name"]: user for user in users}


@pytest_asyncio.fixture(loop_scope="session", scope="function")
async def shop_items(test_db):
    with open("./data_files/shop.json") as file:
        items = json.load(file)

    async with test_db.begin() as connection:
        await connection.execute(insert(db_tables.shop_item).values(items))

    return sorted(items, key=lambda item: item["name"])


@pytest_asyncio.fixture(loop_scope="session", scope="function")
def test_app(test_db):
    return app


@pytest_asyncio.fixture(loop_scope="session", scope="function")
async def client_factory(test_app, user_factory):
    async def create_client(user_name):
        if user_name not in user_factory:
            async with httpx.AsyncClient(
                app=test_app, base_url="http://coup.test"
            ) as client:
                yield client
        else:
            user_data = user_factory[user_name]
            async with httpx.AsyncClient(
                app=test_app, base_url="http://coup.test"
            ) as client:
                result = await client.post(
                    "/auth/login",
                    json={"email": user_data["email"], "password": user_data["password"]},
                )
                assert result.status_code == 200

            data = result.json()

            async with httpx.AsyncClient(
                app=test_app,
                base_url="http://coup.test",
                headers={"Authorization": f"Bearer {data['token']}"},
                follow_redirects=True
            ) as client:
                yield client

    return create_client

@pytest_asyncio.fixture(loop_scope="session", scope="function")
async def amiya_client(client_factory):
    async for item in client_factory("Amiya"):
        yield item
