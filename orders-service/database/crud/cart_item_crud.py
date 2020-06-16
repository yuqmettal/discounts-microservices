from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import CartItem
from database.schema.cart_item_schema import CartItemCreate, CartItemUpdate


class CartItemCRUD(CRUDBase[CartItem, CartItemCreate, CartItemUpdate]):
    pass


cart_item = CartItemCRUD(CartItem)
