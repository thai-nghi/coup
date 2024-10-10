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
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, TEXT

metadata_obj = MetaData()
from src import schemas

user_rank_enum = Enum(schemas.UserRank)

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("full_name", String, nullable=False),
    Column("email", String, nullable=False, unique=True, index=True),
    Column("password", String, nullable=True),
    Column("points", Integer, nullable=False, default=0),
    Column("total_points", Integer, nullable=False, default=0),
    Column("city", String, nullable=False),
    Column("country", String, nullable=False),
    Column("rank", user_rank_enum, nullable=False, default=schemas.UserRank.ROOKIE),
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
    Column("rank_to_unlock", user_rank_enum, nullable=False),
    Column("description", String, nullable=False),
    Column("banner_pic", String, nullable=False),
)

user_inventory = Table(
    "user_inventory",
    metadata_obj,
    Column("user_id", ForeignKey("user.id"), nullable=False),
    Column("item_id", ForeignKey("shop_item.id"), nullable=False),
    Column("quantity", Integer, default=0),
    PrimaryKeyConstraint("user_id", "item_id", name="inventory_pk"),
)

user_point_gain = Table(
    "user_point_gain",
    metadata_obj,
    Column("user_id", ForeignKey("user.id"), nullable=False),
    Column("point", Integer, nullable=False),
    Column(
        "gain_at",
        TIMESTAMP(timezone=True),
        server_default=text("current_timestamp"),
        nullable=False,
    ),
)
