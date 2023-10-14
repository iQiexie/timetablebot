"""make external ids BigInteger

Revision ID: 0009
Revises: 0008
Create Date: 2023-10-14 14:33:50.754273

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "external_users",
        "telegram_id",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=True,
    )
    op.alter_column(
        "external_users",
        "vk_id",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=True,
    )
    op.alter_column("users", "password", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("users_activity", "source", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users_activity", "source", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("users", "password", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        "external_users",
        "vk_id",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )
    op.alter_column(
        "external_users",
        "telegram_id",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
