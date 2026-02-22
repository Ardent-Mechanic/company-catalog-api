from pydantic import BaseModel


class ActivityShort(BaseModel):
    id: int
    name: str
    # можно добавить parent_id
    
    model_config = {
        "from_attributes": True,
        "extra": "ignore",
        # "arbitrary_types_allowed": True # если есть кастомные типы
    }