"""init

Revision ID: 0cdc72413cb6
Revises: 
Create Date: 2023-02-20 09:22:16.376176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0cdc72413cb6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("vk_id", sa.Integer(), nullable=True),
        sa.Column("group_index", sa.Integer(), nullable=True),
        sa.Column("ai_companion_enabled", sa.Boolean(), nullable=True),
        sa.Column("last_activity", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("uuid"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###