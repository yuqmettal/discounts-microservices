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
    


class DiscountCreate(DiscountBase):
    start_date: date
    end_date: date
    calendarized: bool
    priority: int
    discount: float
    retailer_id: int


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

    class Config:
        orm_mode = True


class Discount(DiscountInDatabase):
    pass
