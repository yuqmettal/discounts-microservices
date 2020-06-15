from typing import Optional

from pydantic import BaseModel


class ProvinceBase(BaseModel):
    name: Optional[str] = None
    region: Optional[str] = None
    country_id: Optional[int] = None


class ProvinceCreate(ProvinceBase):
    name: str
    region: str
    country_id: int


class ProvinceUpdate(ProvinceBase):
    pass


class ProvinceInDatabase(ProvinceBase):
    id: int
    name: str
    region: str
    country_id: int

    class Config:
        orm_mode = True


class Province(ProvinceInDatabase):
    pass
