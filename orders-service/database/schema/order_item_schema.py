from typing import Optional

from pydantic import BaseModel


class OrderItemBase(BaseModel):
    order_id: Optional[int] = None
    item_id: Optional[int] = None
    pvp: Optional[float] = None
    quantity: Optional[float] = None
    notes: Optional[str] = None
    pvp_with_discount: Optional[float] = None


class OrderItemCreate(OrderItemBase):
    order_id: int
    item_id: int
    pvp: float
    quantity: float
    notes: str
    pvp_with_discount: float


class OrderItemUpdate(OrderItemBase):
    pass


class OrderItemInDatabase(OrderItemBase):
    id: int
    order_id: int
    item_id: int
    pvp: float
    quantity: float
    notes: str
    pvp_with_discount: float

    class Config:
        orm_mode = True


class OrderItem(OrderItemInDatabase):
    pass
