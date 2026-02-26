from typing import TYPE_CHECKING, List

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base

from geoalchemy2 import Geography  # основной тип для PostGIS

if TYPE_CHECKING:
    from app.core.models.organization import Organization


class Building(Base):
    """
    Здание (Building)
    
    Представляет информацию о конкретном здании, в котором находится организация.
    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String(255), unique=True)

    # Основное пространственное поле точка в координатах (lon, lat)
    # Основное поле — теперь Geography
    geom: Mapped[Geography] = mapped_column(
        Geography(
            geometry_type="POINT",
            srid=4326,
            spatial_index=False   # создаст GIST-индекс
        ),
        nullable=False,
        index=True
    )
    latitude: Mapped[float] = mapped_column(Float, nullable=True) # Обратная совместимость
    longitude: Mapped[float] = mapped_column(Float, nullable=True) # Обратная совместимость

    organizations: Mapped[List["Organization"]] = relationship(back_populates="building", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Building(id={self.id}, address='{self.address}')"
