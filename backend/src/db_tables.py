from sqlalchemy import (Boolean, Column, Enum, Float, ForeignKey, Integer,
                        MetaData, PrimaryKeyConstraint, String, Table, text)
from sqlalchemy.dialects.postgresql import JSONB, TEXT, TIMESTAMP

metadata_obj = MetaData()
from src import schemas

item_type_enum = Enum(schemas.ItemType)
coin_change_enum = Enum(schemas.CoinChangeEventType)
match_type_enum = Enum(schemas.MatchType)
result_enum = Enum(schemas.MatchResult)

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("display_name", String, nullable=False),
    Column("email", String, nullable=False, unique=True, index=True),
    Column("password", String, nullable=True),
    Column("elo", Integer, nullable=False, default=0),
    Column("coins", Integer, nullable=False, default=0),
    Column("country", ForeignKey("countries.id"), nullable=False, index=True),
)

admin_user = Table(
    "admin_user",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("display_name", String, nullable=False),
    Column("email", String, nullable=False, unique=True, index=True),
    Column("password", String, nullable=True),
)


user_google_id = Table(
    "user_google_id",
    metadata_obj,
    Column("google_id", String, primary_key=True),
    Column("user_id", ForeignKey("user.id"), nullable=False),
)


shop_item = Table(
    "shop_item",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("price", Integer, nullable=False),
    Column("description", String, nullable=False),
    Column("banner_pic", String, nullable=False),
    Column("item_type", item_type_enum, nullable=False),
    Column("discount", Float, nullable=False, default=0),
    Column("active", Boolean, nullable=False, default=True),
)

user_inventory = Table(
    "user_inventory",
    metadata_obj,
    Column("user_id", ForeignKey("user.id"), nullable=False, index=True),
    Column("item_id", ForeignKey("shop_item.id"), nullable=False, index=True),
    Column("quantity", Integer, default=0),
    PrimaryKeyConstraint("user_id", "item_id", name="inventory_pk"),
)

matches = Table(
    "matches",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("replay", JSONB, nullable=False),
    Column(
        "match_time",
        TIMESTAMP(timezone=True),
        server_default=text("current_timestamp"),
        nullable=False,
    ),
    Column("type", match_type_enum, nullable=False),
)

player_matches = Table(
    "player_matches",
    metadata_obj,
    Column("player_id", ForeignKey("user.id"), nullable=False, index=True),
    Column("match_id", ForeignKey("matches.id"), nullable=False),
    Column("result", result_enum, nullable=False),
    PrimaryKeyConstraint("player_id", "match_id", name="player_match_pk"),
)


elo_change = Table(
    "elo_change",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("player_id", ForeignKey("user.id"), nullable=False, index=True),
    Column("elo_change", Integer, nullable=False),
    Column("match_id", ForeignKey("matches.id"), nullable=True),
)

coin_change = Table(
    "coin_change",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("player_id", ForeignKey("user.id"), nullable=False),
    Column("coin_change", Integer, nullable=False),
    Column("event_type", coin_change_enum, nullable=True),
    Column("event_id", Integer),
)


countries = Table(
    "countries",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("label", String, nullable=False),
)
