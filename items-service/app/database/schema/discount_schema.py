from datetime import date
from typing import Optional

from pydantic import BaseModel


class DiscountBase(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    calendarized: Optional[bool] = None
    priority: Optional[int] = None
    discount: Optional[float] = None
    retailer_id: Optional[int] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    by_products: Optional[bool] = None
    by_clients: Optional[bool] = None
    to_prime_clients: Optional[bool] = None
    free_shipping: Optional[bool] = None
    free_shipping_amount: Optional[float] = None
    according_deliver_day: Optional[bool] = None
    according_order_day: Optional[bool] = None
    order_and_deliver_same_day: Optional[bool] = None
    


class DiscountCreate(DiscountBase):
    start_date: date
    end_date: date
    calendarized: bool
    priority: int
    discount: float
    retailer_id: int
    category_id: int
    brand_id: int
    subcategory_id: int
    by_products: bool
    by_clients: bool
    to_prime_clients: bool
    free_shipping: bool
    free_shipping_amount: float
    according_deliver_day: bool
    according_order_day: bool
    order_and_deliver_same_day: bool


class DiscountUpdate(DiscountBase):
    pass


class DiscountInDatabase(DiscountBase):
    id: int
    start_date: date
    end_date: date
    calendarized: bool
    priority: int
    discount: float
    retailer_id: int
    category_id: int
    brand_id: int
    subcategory_id: int
    by_products: bool
    by_clients: bool
    to_prime_clients: bool
    free_shipping: bool
    free_shipping_amount: float
    according_deliver_day: bool
    according_order_day: bool
    order_and_deliver_same_day: bool

    class Config:
        orm_mode = True


class Discount(DiscountInDatabase):
    pass
