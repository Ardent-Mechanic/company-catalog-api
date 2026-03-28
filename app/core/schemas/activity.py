from typing import Optional

from pydantic import BaseModel, Field


class ActivityShort(BaseModel):
    id: int
    name: str
    # можно добавить parent_id

    model_config = {
        "from_attributes": True,
        "extra": "ignore",
        # "arbitrary_types_allowed": True # если есть кастомные типы
    }

class ActivityTree(ActivityShort):
    parent_id: Optional[int] = None
    organization_count: int = 0
    children: list["ActivityTree"] = Field(default_factory=list)
