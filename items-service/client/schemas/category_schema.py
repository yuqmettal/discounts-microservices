from typing import Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    name: str
    description: str


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDatabase(CategoryBase):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True


class Category(CategoryInDatabase):
    pass
