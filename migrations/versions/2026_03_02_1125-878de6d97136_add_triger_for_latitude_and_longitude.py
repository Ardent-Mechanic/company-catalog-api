"""add triger for latitude and longitude

Revision ID: 878de6d97136
Revises: 5eed01a43bcd
Create Date: 2026-03-02 11:25:51.955573
Confirmed by:
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import geoalchemy2
import logging

# revision identifiers
revision: str = "878de6d97136"
down_revision: Union[str, Sequence[str], None] = "5eed01a43bcd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

logger = logging.getLogger("alembic.runtime.migration")


def upgrade() -> None:
    logger.info(
        f"=== APPLYING MIGRATION === | "
        f"Revision: {revision} | "
        f"Down: {down_revision} | "
        f"Message: add triger for latitude and longitude"
    )
    
    # 2. Создаём функцию триггера через raw SQL (GeoAlchemy2 специфичные функции)
    op.execute("""
        CREATE OR REPLACE FUNCTION update_building_coords()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Извлекаем координаты из POINT геометрии
            NEW.latitude := ST_Y(NEW.geom::geometry);
            NEW.longitude := ST_X(NEW.geom::geometry);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # 3. Создаём триггер
    op.execute("""
        CREATE TRIGGER building_coords_trigger
            BEFORE INSERT OR UPDATE OF geom ON building
            FOR EACH ROW
            EXECUTE FUNCTION update_building_coords();
    """)

    # 4. Инициализируем координаты для существующих записей
    op.execute("""
        UPDATE building 
        SET latitude = ST_Y(geom::geometry),
            longitude = ST_X(geom::geometry)
        WHERE geom IS NOT NULL;
    """)

    # 5. Делаем колонки NOT NULL после заполнения (опционально, если у всех есть geom)
    # op.alter_column("building", "latitude", nullable=False)
    # op.alter_column("building", "longitude", nullable=False)

    # 6. Создаём индексы для быстрого поиска по координатам
    op.create_index(
        "ix_building_latitude", 
        "building", 
        ["latitude"]
    )
    op.create_index(
        "ix_building_longitude", 
        "building", 
        ["longitude"]
    )
    # Композитный индекс для geo-запросов (опционально)
    op.create_index(
        "ix_building_coords", 
        "building", 
        ["latitude", "longitude"]
    )

    logger.info("Building coordinates trigger and indexes created successfully")


def downgrade() -> None:
    logger.warning(f"=== REVERTING MIGRATION === | " f"Revision: {revision}")
    op.drop_index("ix_building_coords", table_name="building")
    op.drop_index("ix_building_longitude", table_name="building")
    op.drop_index("ix_building_latitude", table_name="building")

    op.execute("DROP TRIGGER IF EXISTS building_coords_trigger ON building;")
    op.execute("DROP FUNCTION IF EXISTS update_building_coords();")
