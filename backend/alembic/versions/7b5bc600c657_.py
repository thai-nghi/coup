"""empty message

Revision ID: 7b5bc600c657
Revises: 
Create Date: 2024-10-13 10:50:41.717692

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7b5bc600c657"
down_revision = None
branch_labels = None
depends_on = None


item_type_enum = postgresql.ENUM(
    "AVATAR_FRAME", "CHESS_BOARD", "CHESS_BACK", "WIN_ANIMATION", "LOSE_ANIMATION", name="item_type_enum", create_type=False
)


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    item_type_enum.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "shop_item",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("banner_pic", sa.String(), nullable=False),
        sa.Column("item_type", item_type_enum, nullable=False),
        sa.Column("discount", sa.Float(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("display_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("elo", sa.Integer(), nullable=False),
        sa.Column("coins", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_table(
        "match_history",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("player_one", sa.Integer(), nullable=False),
        sa.Column("player_two", sa.Integer(), nullable=False),
        sa.Column("replay", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "match_time",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("current_timestamp"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["player_one"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["player_two"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("match_player_one_idx"), "match_history", ["player_one"])
    op.create_index(op.f("match_player_two_idx"), "match_history", ["player_two"])
    op.create_table(
        "user_google_id",
        sa.Column("google_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("google_id"),
    )
    op.create_table(
        "user_inventory",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["shop_item.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "item_id", name="inventory_pk"),
    )
    op.create_table(
        "elo_change",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("elo_change", sa.Integer(), nullable=False),
        sa.Column("match_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["match_id"],
            ["match_history.id"],
        ),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("elo_change")
    op.drop_table("user_inventory")
    op.drop_table("user_google_id")
    op.drop_table("match_history")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_table("shop_item")
    item_type_enum.drop(op.get_bind())
    # ### end Alembic commands ###
