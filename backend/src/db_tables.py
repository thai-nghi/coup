from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Enum,
    text,
    ForeignKey,
    PrimaryKeyConstraint,
    Float,
    Boolean
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, TEXT

metadata_obj = MetaData()
from src import schemas

item_type_enum = Enum(schemas.ItemType)

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("display_name", String, nullable=False),
    Column("email", String, nullable=False, unique=True, index=True),
    Column("password", String, nullable=True),
    Column("elo", Integer, nullable=False, default=0),
    Column("coins", Integer, nullable=False, default=0),
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
    Column("discount", Float, nullable=False, default = 0),
    Column("active", Boolean, nullable=False, default = True)
)

user_inventory = Table(
    "user_inventory",
    metadata_obj,
    Column("user_id", ForeignKey("user.id"), nullable=False),
    Column("item_id", ForeignKey("shop_item.id"), nullable=False),
    Column("quantity", Integer, default=0),
    PrimaryKeyConstraint("user_id", "item_id", name="inventory_pk"),
)

match_history = Table(
    "match_history",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("player_one", ForeignKey("user.id"), nullable=False),
    Column("player_two", ForeignKey("user.id"), nullable=False),
    Column("replay", JSONB, nullable=False),
    Column(
        "match_time",
        TIMESTAMP(timezone=True),
        server_default=text("current_timestamp"),
        nullable=False,
    ),
)

elo_change = Table(
    "elo_change",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("player_id", ForeignKey("user.id"), nullable=False),
    Column("elo_change", Integer, nullable=False),
    Column("match_id", ForeignKey("match_history.id"), nullable=True)
)
