from typing import TYPE_CHECKING, List

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base

if TYPE_CHECKING:
    from app.core.models.organization import Organization


class Building(Base):
    """
    Здание (Building)
    
    Представляет информацию о конкретном здании, в котором находится организация.
    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String(255), unique=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    # One-to-many relationship with Organization
    organizations: Mapped[List["Organization"]] = relationship(back_populates="building", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Building(id={self.id}, address='{self.address}')"
