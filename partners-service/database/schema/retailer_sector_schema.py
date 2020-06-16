from typing import Optional

from pydantic import BaseModel


class RetailerSectorBase(BaseModel):
    sector_id: Optional[int] = None
    retailer_id: Optional[int] = None
    enabled: Optional[bool] = None


class RetailerSectorCreate(RetailerSectorBase):
    sector_id: int
    retailer_id: int
    enabled: bool


class RetailerSectorUpdate(RetailerSectorBase):
    pass


class RetailerSectorInDatabase(RetailerSectorBase):
    id: int
    sector_id: int
    retailer_id: int
    enabled: bool

    class Config:
        orm_mode = True


class RetailerSector(RetailerSectorInDatabase):
    pass
