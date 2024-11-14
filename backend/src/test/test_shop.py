import asyncio

import httpx
import pytest


@pytest.mark.asyncio
async def test_list_shop(amiya_client, shop_items):
    shop_result = await amiya_client.get("/shop")

    assert shop_result.status_code == 200

    items = shop_result.json()

    assert len(items["items"]) == len(shop_items)

    sorted_items = sorted(items["items"], key=lambda item: item["name"])

    for index, item in enumerate(sorted_items):
        assert item["name"] == shop_items[index]["name"]


@pytest.mark.parametrize(
    "user, item_id, expected_status, text",
    (
        pytest.param("Amiya", 1, 200, None, id="buy-success"),
        pytest.param(
            "Amiya",
            2,
            400,
            "User does not have enough coins",
            id="buy-fail-not-enough-coin",
        ),
        pytest.param(
            "unknown", 2, 401, "Not authenticated", id="buy-fail-not-logged-in"
        ),
    ),
)
@pytest.mark.asyncio
async def test_buy_item(
    client_factory, user, item_id, expected_status, text, shop_items
):
    client = await anext(client_factory(user))
    buy_response = await client.post(f"/shop/{item_id}")

    assert buy_response.status_code == expected_status

    if expected_status != 200:
        assert text in buy_response.text
