import pytest
import httpx

@pytest.mark.asyncio
async def test_create_user(test_app):
    async with httpx.AsyncClient(app=test_app, base_url="http://coup.test") as client:
        result = await client.post("/auth/register", json={
            "email": "test@gmail.com",
            "display_name": "Test Full name",
            "country": "test_country",
            "password": "123",
            "confirm_password": "123"
        })
        assert result.status_code == 200

        data = result.json()

        print(data)

        assert 0 == 1