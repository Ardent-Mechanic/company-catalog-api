from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base

if TYPE_CHECKING:
    from app.core.models.organization import Organization


class Activity(Base):
    """
    Деятельность (Activity/Business Type)
    
    Позволяет классифицировать род деятельности организаций в каталоге.
    Имеет древовидную структуру, где каждая деятельность может содержать подвиды.
    
    Пример структуры:
    - Еда
      - Мясная продукция
      - Молочная продукция
    - Автомобили
      - Грузовые
      - Легковые
        - Запчасти
        - Аксессуары
    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("activity.id", ondelete="CASCADE"), default=None)

    # Self-referential relationships
    parent: Mapped[Optional["Activity"]] = relationship(
        back_populates="children",
        remote_side=[id],
        foreign_keys=[parent_id]
    )
    children: Mapped[List["Activity"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    # Relationship with Organization
    organizations: Mapped[List["Organization"]] = relationship(
        secondary="organization_activity",
        back_populates="activities"
    )

    def __repr__(self) -> str:
        return f"Activity(id={self.id}, name='{self.name}', parent_id={self.parent_id})"
