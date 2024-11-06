import pytest
import httpx
import asyncio


@pytest.mark.asyncio
async def test_create_user(authenticated_client):
    shop_result = await authenticated_client.get("/shop")

    assert shop_result.status_code == 200