from typing import Optional

from pydantic import BaseModel


class SubcategoryBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None


class SubcategoryCreate(SubcategoryBase):
    name: str
    description: str
    category_id: int


class SubcategoryUpdate(SubcategoryBase):
    pass


class SubcategoryInDatabase(SubcategoryBase):
    id: int
    name: str
    description: str
    category_id: int

    class Config:
        orm_mode = True


class Subcategory(SubcategoryInDatabase):
    pass
