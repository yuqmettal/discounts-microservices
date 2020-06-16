from typing import Optional

from pydantic import BaseModel


class PrimeSubscriptionBase(BaseModel):
    name: Optional[str] = None
    validity: Optional[int] =None
    validity_type: Optional[str] = None
    enabled: Optional[bool] = None


class PrimeSubscriptionCreate(PrimeSubscriptionBase):
    name: str
    validity: int
    validity_type: str
    enabled: bool


class PrimeSubscriptionUpdate(PrimeSubscriptionBase):
    pass


class PrimeSubscriptionInDatabase(PrimeSubscriptionBase):
    id: int
    name: str
    validity: int
    validity_type: str
    enabled: bool

    class Config:
        orm_mode = True


class PrimeSubscription(PrimeSubscriptionInDatabase):
    pass
