from typing import Optional

from pydantic import BaseModel


class DiscountItemBase(BaseModel):
    discount_id: Optional[int] = None
    item_id: Optional[int] = None


class DiscountItemCreate(DiscountItemBase):
    discount_id: int
    item_id: int


class DiscountItemUpdate(DiscountItemBase):
    pass


class DiscountItemInDatabase(DiscountItemBase):
    id: int
    discount_id: int
    item_id: int

    class Config:
        orm_mode = True


class DiscountItem(DiscountItemInDatabase):
    pass
