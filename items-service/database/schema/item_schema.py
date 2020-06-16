from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    retailer_id: Optional[int] = None
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    pvp: Optional[float] = None
    margin: Optional[float] = None


class ItemCreate(ItemBase):
    retailer_id: int
    product_id: int
    category_id: int
    pvp: float
    margin: float


class ItemUpdate(ItemBase):
    pass


class ItemInDatabase(ItemBase):
    id: int
    retailer_id: int
    product_id: int
    category_id: int
    pvp: float
    margin: float

    class Config:
        orm_mode = True


class Item(ItemInDatabase):
    pass
