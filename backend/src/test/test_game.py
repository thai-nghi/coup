import httpx
import pytest
from src import schemas
from src.schemas import response


@pytest.mark.asyncio
async def test_submit_result(test_app, test_settings, amiya_client):

    amiya_profile_response = await amiya_client.get("/user/")
    amiya_profile_start = amiya_profile_response.json()

    async with httpx.AsyncClient(
        app=test_app,
        base_url="http://coup.test",
        headers={"Authorization": f"Bearer {test_settings.GAME_SERVER_ACCESS}"},
    ) as client:
        response = await client.post(
            "/admin/game/result",
            json={
                "match_id": 1,
                "match_replay": "",
                "move_first_player": 1,
                "player_result": [
                    {
                        "player_id": 1,
                        "elo_change": 10,
                        "result": schemas.MatchResult.WIN.value,
                        "coin_change": 50,
                    },
                    {
                        "player_id": 2,
                        "elo_change": -10,
                        "result": schemas.MatchResult.LOSE.value,
                        "coin_change": 10,
                    },
                ],
                "type": schemas.MatchType.RANKED.value,
            },
        )

    assert response.status_code == 200

    amiya_profile_response = await amiya_client.get("/user/")
    amiya_profile_after = amiya_profile_response.json()

    assert amiya_profile_start["elo"] + 10 == amiya_profile_after["elo"]
    assert amiya_profile_start["coins"] + 50 == amiya_profile_after["coins"]


@pytest.mark.parametrize(
    "player, expected_win, expected_loss, expected_total",
    (pytest.param("Amiya", 3, 0, 3), pytest.param("Blaze", 0, 3, 3)),
)
@pytest.mark.asyncio
async def test_match_history_summary(
    client_factory, player, expected_win, expected_loss, expected_total, match_history
):
    client = await anext(client_factory(player))

    history_summary_response = await client.get("/game/history_summary")

    assert history_summary_response.status_code == 200

    summary_data = response.MatchHistorySummary(**history_summary_response.json())

    assert summary_data.win == expected_win
    assert summary_data.loss == expected_loss
    assert summary_data.total_match == expected_total


@pytest.mark.asyncio
async def test_match_history(amiya_client, match_history):
    history_response = await amiya_client.get("game/history")

    assert history_response.status_code == 200

    history_data = response.MatchHistory(**history_response.json())

    assert history_data.page == 1
    assert history_data.page_size == 20
    print(history_data.matches)
    assert len(history_data.matches) == 3
