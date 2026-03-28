"""enable postgis

Revision ID: 4bd966d063c2
Revises:
Create Date: 2026-02-25 13:21:19.552884
Confirmed by: Green <test@example.com> 
"""

from typing import Sequence, Union
from alembic import op
import logging

revision: str = "4bd966d063c2"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

logger = logging.getLogger("alembic.runtime.migration")


def upgrade() -> None:
    logger.info(
        f"=== APPLYING MIGRATION === | "
        f"Revision: {revision} | "
        f"Down: {down_revision} | "
        f"Message: enable postgis"
    )
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")


def downgrade() -> None:
    logger.warning(f"=== REVERTING MIGRATION === | " f"Revision: {revision}")
    op.execute("DROP EXTENSION IF EXISTS postgis CASCADE")
