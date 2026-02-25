"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
Confirmed by:
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import geoalchemy2
import logging

${imports if imports else ""}

# revision identifiers
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}

logger = logging.getLogger("alembic.runtime.migration")


def upgrade() -> None:
    logger.info(
        f"=== APPLYING MIGRATION === | "
        f"Revision: {revision} | "
        f"Down: {down_revision} | "
        f"Message: ${message}"
    )
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    logger.warning(
        f"=== REVERTING MIGRATION === | "
        f"Revision: {revision}"
    )
    ${downgrades if downgrades else "pass"}