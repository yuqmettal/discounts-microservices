from typing import Optional

from pydantic import BaseModel


class BrandBase(BaseModel):
    name: Optional[str] = None


class BrandCreate(BrandBase):
    name: str


class BrandUpdate(BrandBase):
    pass


class BrandInDatabase(BrandBase):
    id: int
    name: str

    class Config:
        orm_mode = True


class Brand(BrandInDatabase):
    pass
