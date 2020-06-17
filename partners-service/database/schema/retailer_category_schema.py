from typing import Optional

from pydantic import BaseModel


class RetailerCategoryBase(BaseModel):
    category_id: Optional[int] = None
    retailer_id: Optional[int] = None
    enabled: Optional[bool] = None


class RetailerCategoryCreate(RetailerCategoryBase):
    category_id: int
    retailer_id: int
    enabled: bool


class RetailerCategoryUpdate(RetailerCategoryBase):
    pass


class RetailerCategoryInDatabase(RetailerCategoryBase):
    id: int
    category_id: int
    retailer_id: int
    enabled: bool

    class Config:
        orm_mode = True


class RetailerCategory(RetailerCategoryInDatabase):
    pass
