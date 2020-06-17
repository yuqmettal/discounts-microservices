from typing import Optional

from pydantic import BaseModel


class RetailerBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    city_id: Optional[int] = None


class RetailerCreate(RetailerBase):
    name: str
    description: str
    city_id: int


class RetailerUpdate(RetailerBase):
    pass


class RetailerInDatabase(RetailerBase):
    id: int
    name: str
    description: str
    city_id: int

    class Config:
        orm_mode = True


class Retailer(RetailerInDatabase):
    pass
