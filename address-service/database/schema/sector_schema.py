from typing import Optional

from pydantic import BaseModel


class SectorBase(BaseModel):
    name: Optional[str] = None
    city_id: Optional[int] = None


class SectorCreate(SectorBase):
    name: str
    city_id: int


class SectorUpdate(SectorBase):
    pass


class SectorInDatabase(SectorBase):
    id: int
    name: str
    city_id: int

    class Config:
        orm_mode = True


class Sector(SectorInDatabase):
    pass
