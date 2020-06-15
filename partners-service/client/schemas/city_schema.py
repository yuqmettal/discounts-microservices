from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    name: Optional[str] = None
    province_id: Optional[int] = None


class CityInsert(CityBase):
    id: int
    name: str
    province_id: int


class CityCreate(CityBase):
    name: str
    province_id: int


class CityUpdate(CityBase):
    pass


class CityInDatabase(CityBase):
    id: int
    name: str
    province_id: int

    class Config:
        orm_mode = True


class City(CityInDatabase):
    pass
