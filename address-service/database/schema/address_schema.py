from typing import Optional

from pydantic import BaseModel


class AddressBase(BaseModel):
    name: Optional[str] = None
    sector_id: Optional[int] = None
    line_one: Optional[str] = None
    line_two: Optional[str] = None


class AddressCreate(AddressBase):
    name: str
    sector_id: int
    line_one: str
    line_two: str


class AddressUpdate(AddressBase):
    pass


class AddressInDatabase(AddressBase):
    id: int
    name: str
    sector_id: int
    line_one: str
    line_two: str

    class Config:
        orm_mode = True


class Address(AddressInDatabase):
    pass
