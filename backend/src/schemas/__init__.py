import enum
from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, field_validator, model_validator


class UserRank(enum.Enum):
    ROOKIE = 1
    CADET = 2
    WARRIOR = 3
    CHAMPION = 4
    LEGEND = 5


class ItemType(enum.Enum):
    AVATAR_FRAME = 1
    CHESS_BOARD = 2
    CHESS_BACK = 3
    WIN_ANIMATION = 4
    LOSE_ANIMATION = 5


class CoinChangeEventType(enum.Enum):
    MATCH = 1
    SHOP = 2
    PROMOTION = 3
    ADMIN = 4


class MatchResult(enum.Enum):
    LOSE = 0
    WIN = 1


class MatchType(enum.Enum):
    RANKED = 0
    LOBBY = 1


class MetadataFields(str, enum.Enum):
    COUNTRY = "COUNTRY"


class Country(BaseModel):
    label: str
    value: int


class UserBase(BaseModel):
    email: EmailStr
    display_name: str
    country_id: int


class UserCreate(UserBase):
    password: str | None = None


class UserResponse(UserBase):
    id: int
    elo: int
    coins: int


class GoogleCredentalData(BaseModel):
    sub: str
    email: str
    given_name: str
    family_name: str
    picture: str


class UserRegister(UserBase):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def verify_password_match(self):

        pw1 = self.password
        pw2 = self.confirm_password

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("The two passwords did not match.")

        return self


class UserLogin(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    google_token: str | None = None

    @model_validator(mode="before")
    @classmethod
    def ensure_credentals(cls, values):
        if "username" in values:
            values["email"] = values["username"]
        if "email" not in values and "google_token" not in values:
            raise ValueError("Either email or google_token is needed")
        if "email" in values and "password" not in values:
            raise ValueError("Password is required for login with email")

        return values


class JwtTokenSchema(BaseModel):
    token: str
    payload: dict
    expire: datetime


class TokenPair(BaseModel):
    access: JwtTokenSchema
    refresh: JwtTokenSchema


class SuccessResponseScheme(BaseModel):
    msg: str


class LeaderboardEntry(BaseModel):
    total_points: int
    full_name: str
    rank: UserRank
    id: int


class ShopItem(BaseModel):
    id: int
    name: str
    description: str
    price: int
    banner_pic: str
    item_type: ItemType


class PlayerResult(BaseModel):
    player_id: int
    elo_change: int
    result: MatchResult
    coin_change: int


class MatchResultIn(BaseModel):
    match_id: str
    match_replay: str
    move_first_player: int
    player_result: list[PlayerResult]
    type: MatchType


class MatchHistoryEntry(PlayerResult):
    match_id: int
    match_time: datetime
    type: MatchType


class PlayerSummary(BaseModel):
    player_id: int
    display_name: str
    elo: int


class NewMatchData(BaseModel):
    match_id: str
    player_data: list[PlayerSummary]


class ItemCategory(BaseModel):
    name: str
    items: list[ShopItem]
