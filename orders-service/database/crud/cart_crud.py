from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import Cart
from database.schema.cart_schema import CartCreate, CartUpdate


class CartCRUD(CRUDBase[Cart, CartCreate, CartUpdate]):
    pass


cart = CartCRUD(Cart)
