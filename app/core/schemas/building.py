from pydantic import BaseModel


class BuildingShort(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    model_config = {
        "from_attributes": True,
        "extra": "ignore",
        # "arbitrary_types_allowed": True # если есть кастомные типы
    }
