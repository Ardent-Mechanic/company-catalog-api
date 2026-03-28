"""init db

Revision ID: 69d463712ba9
Revises: 4bd966d063c2
Create Date: 2026-02-25 15:36:24.763082
Confirmed by: Green <test@example.com>
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import geoalchemy2
import logging

revision: str = "69d463712ba9"
down_revision: Union[str, Sequence[str], None] = "4bd966d063c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

logger = logging.getLogger("alembic.runtime.migration")


def upgrade() -> None:
    logger.info(
        f"=== APPLYING MIGRATION === | "
        f"Revision: {revision} | "
        f"Down: {down_revision} | "
        f"Message: init db"
    )
    op.create_table(
        "activity",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["activity.id"],
            name=op.f("fk_activity_parent_id_activity"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_activity")),
        sa.UniqueConstraint("name", name=op.f("uq_activity_name")),
    )
    op.create_index(op.f("ix_activity_id"), "activity", ["id"], unique=False)
    op.create_table(
        "building",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column(
            "geom",
            geoalchemy2.types.Geography(
                geometry_type="POINT",
                srid=4326,
                dimension=2,
                spatial_index=False,
                from_text="ST_GeogFromText",
                name="geography",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_building")),
        sa.UniqueConstraint("address", name=op.f("uq_building_address")),
    )
    op.create_index(
        op.f("ix_building_geom"), "building", ["geom"], unique=False
    )
    op.create_index(op.f("ix_building_id"), "building", ["id"], unique=False)
    op.create_table(
        "organization",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["building_id"],
            ["building.id"],
            name=op.f("fk_organization_building_id_building"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_organization")),
    )
    op.create_index(
        op.f("ix_organization_id"), "organization", ["id"], unique=False
    )
    op.create_table(
        "organization_activity",
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["activity_id"],
            ["activity.id"],
            name=op.f("fk_organization_activity_activity_id_activity"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name=op.f("fk_organization_activity_organization_id_organization"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "organization_id",
            "activity_id",
            name=op.f("pk_organization_activity"),
        ),
    )
    op.create_table(
        "phone_number",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name=op.f("fk_phone_number_organization_id_organization"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_phone_number")),
    )
    op.create_index(
        op.f("ix_phone_number_id"), "phone_number", ["id"], unique=False
    )


def downgrade() -> None:
    logger.warning(f"=== REVERTING MIGRATION === | " f"Revision: {revision}")
    op.drop_index(op.f("ix_phone_number_id"), table_name="phone_number")
    op.drop_table("phone_number")
    op.drop_table("organization_activity")
    op.drop_index(op.f("ix_organization_id"), table_name="organization")
    op.drop_table("organization")
    op.drop_index(op.f("ix_building_id"), table_name="building")
    op.drop_index(op.f("ix_building_geom"), table_name="building")
    op.drop_table("building")
    op.drop_index(op.f("ix_activity_id"), table_name="activity")
    op.drop_table("activity")
