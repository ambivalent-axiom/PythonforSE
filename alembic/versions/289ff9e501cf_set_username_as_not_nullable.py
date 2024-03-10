"""Set username as not nullable

Revision ID: 289ff9e501cf
Revises: 05f2977884e4
Create Date: 2024-02-24 13:26:28.167740

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "289ff9e501cf"
down_revision: Union[str, None] = "05f2977884e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("user", "username", nullable=False)
    op.alter_column("user", "short_description", nullable=False)
    op.add_column("user", sa.Column("test", sa.String()))


def downgrade() -> None:
    op.drop_column("user", "test")
    op.alter_column("user", "short_description", nullable=True)
    op.alter_column("user", "username", nullable=True)
