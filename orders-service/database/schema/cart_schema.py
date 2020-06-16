from typing import Optional

from pydantic import BaseModel


class CartBase(BaseModel):
    name: Optional[str] = None


class CartCreate(CartBase):
    name: str


class CartUpdate(CartBase):
    pass


class CartInDatabase(CartBase):
    id: int
    name: str

    class Config:
        orm_mode = True


class Cart(CartInDatabase):
    pass
