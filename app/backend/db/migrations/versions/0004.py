"""add telemetry

Revision ID: 0004
Revises: 0003
Create Date: 2023-09-03 15:54:53.754863

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "external_users",
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("telegram_id", sa.Integer(), nullable=True),
        sa.Column("vk_id", sa.Integer(), nullable=True),
        sa.Column("group_number", sa.Integer(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram_id"),
        sa.UniqueConstraint("vk_id"),
    )
    op.create_index(op.f("ix_external_users_id"), "external_users", ["id"], unique=False)
    op.create_table(
        "users_activity",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("action", sa.String(), nullable=True),
        sa.Column("requested_day", sa.Date(), nullable=True),
        sa.Column("requested_group", sa.Integer(), nullable=True),
        sa.Column("current_group", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["external_users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_activity_id"), "users_activity", ["id"], unique=False)
    op.create_index(op.f("ix_users_activity_user_id"), "users_activity", ["user_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_activity_user_id"), table_name="users_activity")
    op.drop_index(op.f("ix_users_activity_id"), table_name="users_activity")
    op.drop_table("users_activity")
    op.drop_index(op.f("ix_external_users_id"), table_name="external_users")
    op.drop_table("external_users")
    # ### end Alembic commands ###
