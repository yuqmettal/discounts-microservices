from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import Product
from database.schema.product_schema import ProductCreate, ProductUpdate


class ProductCRUD(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(Product).filter(Product.name == name).first()


product = ProductCRUD(Product)
