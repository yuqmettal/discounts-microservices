from datetime import date
from typing import Optional

from pydantic import BaseModel


class OrderBase(BaseModel):
    retailer_id: Optional[int] = None
    address_id: Optional[int] = None
    client_id: Optional[int] = None
    total_cost: Optional[float] = None
    shipping_cost: Optional[float] = None
    delivery_date: Optional[date] = None


class OrderCreate(OrderBase):
    retailer_id: int
    address_id: int
    client_id: int
    total_cost: float
    shipping_cost: float
    delivery_date: date


class OrderUpdate(OrderBase):
    pass


class OrderInDatabase(OrderBase):
    id: int
    retailer_id: int
    address_id: int
    client_id: int
    total_cost: float
    shipping_cost: float
    delivery_date: date

    class Config:
        orm_mode = True


class Order(OrderInDatabase):
    pass
