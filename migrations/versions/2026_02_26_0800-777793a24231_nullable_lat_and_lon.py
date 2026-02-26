"""nullable lat and lon

Revision ID: 777793a24231
Revises: 69d463712ba9
Create Date: 2026-02-26 08:00:35.382859
Confirmed by:
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import geoalchemy2
import logging

revision: str = "777793a24231"
down_revision: Union[str, Sequence[str], None] = "69d463712ba9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

logger = logging.getLogger("alembic.runtime.migration")


def upgrade() -> None:
    logger.info(
        f"=== APPLYING MIGRATION === | "
        f"Revision: {revision} | "
        f"Down: {down_revision} | "
        f"Message: nullable lat and lon"
    )
    op.alter_column(
        "building",
        "latitude",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )
    op.alter_column(
        "building",
        "longitude",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )


def downgrade() -> None:
    logger.warning(f"=== REVERTING MIGRATION === | " f"Revision: {revision}")
    op.alter_column(
        "building",
        "longitude",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
    op.alter_column(
        "building",
        "latitude",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
