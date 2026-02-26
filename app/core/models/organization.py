from typing import TYPE_CHECKING, Annotated, List

from sqlalchemy import String, ForeignKey, null
from sqlalchemy.orm import Mapped, mapped_column, query_expression, relationship

from app.core.models.base import Base

if TYPE_CHECKING:
    from app.core.models.building import Building
    from app.core.models.activity import Activity

class OrganizationActivity(Base):
    """Связь между организацией и деятельностью (Organization-Activity Association)
    Представляет собой таблицу связи между организациями и видами деятельности. 
    Каждая запись указывает, что определенная организация занимается определенной деятельностью.
    """
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activity.id",  ondelete="CASCADE"), primary_key=True)

    def __repr__(self) -> str:
        return f"OrganizationActivity(organization_id={self.organization_id}, activity_id={self.activity_id})"

class PhoneNumber(Base):
    """
    Номер телефона (Phone Number)
    
    Представляет номер телефона организации.
    Организация может иметь несколько номеров телефонов.
    """
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    phone: Mapped[str] = mapped_column(String(20))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"))

    organization: Mapped["Organization"] = relationship(back_populates="phone_numbers")

    def __repr__(self) -> str:
        return f"PhoneNumber(id={self.id}, phone='{self.phone}')"


# Добавляем типпизцию временного поля для хранения расстояния при поиске nearby
Distance = Annotated[float | None, query_expression(default_expr=null())]

class Organization(Base):
    """
    Организация (Organization)
    Представляет собой карточку организации в справочнике.
    Содержит информацию о названии, контактных номерах, месте расположения и видах деятельности.
    """
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id", ondelete="RESTRICT"))

    building: Mapped["Building"] = relationship(back_populates="organizations")

    distance: Mapped[Distance] = query_expression(default_expr=null())  # Временное поле для хранения расстояния при поиске nearby
    
    phone_numbers: Mapped[List[PhoneNumber]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan"
    )
    activities: Mapped[List["Activity"]] = relationship(
        secondary="organization_activity",
        back_populates="organizations"
    )

    def __repr__(self) -> str:
        return f"Organization(id={self.id}, name='{self.name}', building_id={self.building_id})"
