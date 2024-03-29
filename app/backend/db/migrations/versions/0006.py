"""add legacy user_count

Revision ID: 0006
Revises: 0005
Create Date: 2023-09-04 18:31:01.256660

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.create_unique_constraint("users_username_unique", "users", ["username"])
    op.drop_column("users", "email")

    op.execute(
        """-- auto-generated definition
        create table users_activity_legacy
        (
            id         serial
                primary key,
            date       timestamp,
            user_count integer not null
        );"""
    )

    op.execute(
        """create index ix_users_activity_legacy_id
        on users_activity_legacy (id);"""
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint("users_username_unique", "users", type_="unique")
    op.create_index("ix_users_username", "users", ["username"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    # ### end Alembic commands ###
