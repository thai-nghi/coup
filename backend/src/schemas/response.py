from typing import Any

from pydantic import BaseModel
from src import schemas


class MatchHistory(BaseModel):
    page: int
    page_size: int
    matches: list[schemas.MatchHistoryEntry]


class MatchHistorySummary(BaseModel):
    win: int
    loss: int
    total_match: int
