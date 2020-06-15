from typing import Optional

from pydantic import BaseModel


class CountryBase(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    language: Optional[str] = None
    currency: Optional[str] = None


class CountryInsert(CountryBase):
    id: int
    name: str
    code: str
    language: str
    currency: str


class CountryCreate(CountryBase):
    name: str
    code: str
    language: str
    currency: str


class CountryUpdate(CountryBase):
    pass


class CountryInDatabase(CountryBase):
    id: int
    name: str
    code: str
    language: str
    currency: str

    class Config:
        orm_mode = True


class Country(CountryInDatabase):
    pass
