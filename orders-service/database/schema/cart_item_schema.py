from typing import Optional

from pydantic import BaseModel


class CartItemBase(BaseModel):
    cart_id: Optional[int] = None
    quantity: Optional[float] = None
    notes: Optional[str] = None
    item_id: Optional[int] = None


class CartItemCreate(CartItemBase):
    cart_id: int
    quantity: float
    notes: str
    item_id: int


class CartItemUpdate(CartItemBase):
    pass


class CartItemInDatabase(CartItemBase):
    id: int
    cart_id: int
    quantity: float
    notes: str
    item_id: int

    class Config:
        orm_mode = True


class CartItem(CartItemInDatabase):
    pass
