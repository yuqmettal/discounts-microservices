from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import ClientCart
from database.schema.client_cart_schema import ClientCartCreate, ClientCartUpdate


class ClientCartCRUD(CRUDBase[ClientCart, ClientCartCreate, ClientCartUpdate]):
    pass


client_cart = ClientCartCRUD(ClientCart)
