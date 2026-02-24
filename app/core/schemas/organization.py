from typing import List, Optional

from pydantic import BaseModel, Field

class PhoneNumberOut(BaseModel):
    phone: str

    model_config = {
        "from_attributes": True,
        "extra": "ignore",
        # "arbitrary_types_allowed": True # если есть кастомные типы
    }

class OrganizationFilter(BaseModel):
    # Текстовый поиск (по названию, описанию)
    q: Optional[str] = None
    # По activity (id вида деятельности)
    activity_id: Optional[int] = None
    activity_ids: Optional[List[int]] = None
    # По зданию
    building_id: Optional[int] = None
    # Геометрические фильтры
    lat: Optional[float] = None
    lon: Optional[float] = None
    radius_km: Optional[float] = None
    # Bounding box (прямоугольник)
    min_lat: Optional[float] = None
    max_lat: Optional[float] = None
    min_lon: Optional[float] = None
    max_lon: Optional[float] = None

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    sort: Optional[str] = Field(
        None,
        pattern=r"^(name|distance|rating|created_at)(:(asc|desc))?$"
    )

class CombineOrgFilterPagination(OrganizationFilter, PaginationParams):
    pass

class OrganizationOut(BaseModel):
    id: int
    name: str
    building: "BuildingShort"
    activities: List["ActivityShort"]
    phone_numbers: List[PhoneNumberOut]
    distance_km: Optional[float] = None  # если искали по координатам
    model_config = {
        "from_attributes": True,
        "extra": "ignore",
        # "arbitrary_types_allowed": True # если есть кастомные типы
    }

# Импортируем внизу, чтобы не было циклов
from .building import BuildingShort
from .activity import ActivityShort

# После того как все классы импортированы, Pydantic пересобирает модели
OrganizationOut.model_rebuild()