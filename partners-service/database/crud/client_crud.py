from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import Client
from database.schema.client_schema import ClientCreate, ClientUpdate


class ClientCRUD(CRUDBase[Client, ClientCreate, ClientUpdate]):
    def get_by_email(self, db: Session, *, email: str):
        return db.query(Client).filter(Client.email == email).first()


client = ClientCRUD(Client)
