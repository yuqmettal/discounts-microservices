from typing import Optional
from datetime import date

from pydantic import BaseModel


class ClientPrimeSubscriptionBase(BaseModel):
    activation_date: Optional[date] = None
    subscription_state: Optional[str] = None
    client_id: Optional[int] =None
    prime_subscription_id: Optional[int] = None


class ClientPrimeSubscriptionCreate(ClientPrimeSubscriptionBase):
    activation_date: date
    subscription_state: str
    client_id: int
    prime_subscription_id: int


class ClientPrimeSubscriptionUpdate(ClientPrimeSubscriptionBase):
    pass


class ClientPrimeSubscriptionInDatabase(ClientPrimeSubscriptionBase):
    id: int
    activation_date: date
    subscription_state: str
    client_id: int
    prime_subscription_id: int

    class Config:
        orm_mode = True


class ClientPrimeSubscription(ClientPrimeSubscriptionInDatabase):
    pass
