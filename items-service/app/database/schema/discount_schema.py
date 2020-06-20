from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class DiscountBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    calendarized: Optional[bool] = None
    priority: Optional[int] = None
    discount: Optional[float] = None
    retailer_id: Optional[int] = None
    by_categories: Optional[bool] = None
    by_subcategories: Optional[bool] = None
    by_brands: Optional[bool] = None
    by_products: Optional[bool] = None
    by_clients: Optional[bool] = None
    to_prime_clients: Optional[bool] = None
    free_shipping: Optional[bool] = None
    free_shipping_amount: Optional[float] = None
    according_deliver_day: Optional[bool] = None
    according_order_day: Optional[bool] = None
    order_and_deliver_same_day: Optional[bool] = None


class DiscountCreate(DiscountBase):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    calendarized: bool
    priority: int
    discount: float
    retailer_id: Optional[int] = None
    by_categories: Optional[bool] = None
    by_subcategories: Optional[bool] = None
    by_brands: Optional[bool] = None
    by_products: bool
    by_clients: bool
    to_prime_clients: bool
    free_shipping: bool
    free_shipping_amount: float
    according_deliver_day: bool
    according_order_day: bool
    order_and_deliver_same_day: bool


class DiscountPOST(BaseModel):
    discount: DiscountCreate
    categories: Optional[List] = None
    subcategories: Optional[List] = None
    brands: Optional[List] = None
    products: Optional[List] = None
    

class DiscountUpdate(DiscountBase):
    pass


class DiscountInDatabase(DiscountBase):
    id: int
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    calendarized: bool
    priority: int
    discount: float
    retailer_id: int
    by_categories:bool
    by_subcategories:bool
    by_brands:bool
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
