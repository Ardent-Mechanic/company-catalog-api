from pydantic import BaseModel


class BuildingShort(BaseModel):
    id: int
    address: str
    # latitude и longitude можно не отдавать, если не нужны
    # или добавить distance_km отдельно в OrganizationOut

    model_config = {
        "from_attributes": True,
        "extra": "ignore",
        # "arbitrary_types_allowed": True # если есть кастомные типы
    }