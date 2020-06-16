from typing import Optional

from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class ClientCreate(ClientBase):
    name: str
    last_name: str
    email: EmailStr


class ClientUpdate(ClientBase):
    pass


class ClientInDatabase(ClientBase):
    id: int
    name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class Client(ClientInDatabase):
    pass
