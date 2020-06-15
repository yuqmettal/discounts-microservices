from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import Category
from database.schema.category_schema import CategoryCreate, CategoryUpdate


class CategoryCRUD(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(Category).filter(Category.name == name).first()


category = CategoryCRUD(Category)
