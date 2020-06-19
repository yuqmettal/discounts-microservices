from typing import Optional, List

from pydantic import BaseModel


class RetailerBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    city_id: Optional[int] = None
    category_id: Optional[int] = None
    category_enabled: Optional[bool] = None


class RetailerCreate(RetailerBase):
    name: str
    description: str
    city_id: int
    category_id: int
    category_enabled: bool


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


class RetailerIds(BaseModel):
    ids: List
