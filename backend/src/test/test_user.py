import pytest
import httpx
import asyncio


@pytest.mark.asyncio
async def test_create_user(test_app):
    new_user_data = {
        "email": "test@gmail.com",
        "display_name": "Test Full name",
        "country_id": 10,
    }
    
    async with httpx.AsyncClient(app=test_app, base_url="http://coup.test") as client:
        result = await client.post("/auth/register", json={
            **new_user_data,
            "password": "123",
            "confirm_password": "123"
        })
        assert result.status_code == 200

        data = result.json()

        user = data["user_detail"]

        for key, value in new_user_data.items():
            assert user[key] == value

@pytest.mark.asyncio
async def test_login(test_app):
    new_user_data = {
        "email": "test@gmail.com",
        "display_name": "Test Full name",
        "country_id": 10,
    }
    
    async with httpx.AsyncClient(app=test_app, base_url="http://coup.test") as client:
        result = await client.post("/auth/register", json={
            **new_user_data,
            "password": "456",
            "confirm_password": "456"
        })
        assert result.status_code == 200

        login_result = await client.post("/auth/login", json={
            "email": "test@gmail.com",
            "password": "456"
        })

        print(login_result.text)

        assert login_result.status_code == 200

        data = login_result.json()

        user = data["user_detail"]

        for key, value in new_user_data.items():
            assert user[key] == value