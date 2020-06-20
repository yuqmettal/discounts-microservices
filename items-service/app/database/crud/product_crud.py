from sqlalchemy.orm import Session

from .base import CRUDBase
from app.database.models import Product
from app.database.schema.product_schema import ProductCreate, ProductUpdate


class ProductCRUD(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(Product).filter(Product.name == name).first()

    def filter_by_name(self, db: Session, *, name: str):
        search = "%{}%".format(name)
        return db.query(Product).filter(Product.name.like(search)).all()


product = ProductCRUD(Product)
