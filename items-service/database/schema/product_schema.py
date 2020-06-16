from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tax_rate: Optional[float] = None
    brand_id: Optional[int] = None


class ProductCreate(ProductBase):
    name: str
    description: str
    tax_rate: float
    brand_id: int


class ProductUpdate(ProductBase):
    pass


class ProductInDatabase(ProductBase):
    id: int
    name: str
    description: str
    tax_rate: float
    brand_id: int

    class Config:
        orm_mode = True


class Product(ProductInDatabase):
    pass
