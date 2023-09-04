"""add class model

Revision ID: 0003
Revises: 0002
Create Date: 2023-09-03 12:39:51.959314

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "classes",
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("group_number", sa.Integer(), nullable=False),
        sa.Column("week_day", sa.String(), nullable=False),
        sa.Column("line_position", sa.String(), nullable=False),
        sa.Column("duration", sa.String(), nullable=False),
        sa.Column("row_index", sa.Integer(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("group_number", "week_day", "line_position", "duration", "row_index"),
    )
    op.create_index(op.f("ix_classes_group_number"), "classes", ["group_number"], unique=False)
    op.create_index(op.f("ix_classes_id"), "classes", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_classes_id"), table_name="classes")
    op.drop_index(op.f("ix_classes_group_number"), table_name="classes")
    op.drop_table("classes")
    # ### end Alembic commands ###