from datetime import date
from typing import Optional

from pydantic import BaseModel


class ClientCartBase(BaseModel):
    cart_id: Optional[int] = None
    date_joined: Optional[date] = None
    client_id: Optional[int] = None


class ClientCartCreate(ClientCartBase):
    cart_id: int
    date_joined: date
    client_id: int


class ClientCartUpdate(ClientCartBase):
    pass


class ClientCartInDatabase(ClientCartBase):
    id: int
    cart_id: int
    date_joined: date
    client_id: int

    class Config:
        orm_mode = True


class ClientCart(ClientCartInDatabase):
    pass
