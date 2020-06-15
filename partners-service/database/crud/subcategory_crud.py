from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_

from .base import CRUDBase
from database.models import Subcategory
from database.schema.subcategory_schema import SubcategoryCreate, SubcategoryUpdate


class SubcategoryCRUD(CRUDBase[Subcategory, SubcategoryCreate, SubcategoryUpdate]):
    def get_by_name_and_category_id(self, db: Session, *, name: str, category_id: int):
        return db.query(Subcategory).filter(and_(
            Subcategory.name == name,
            Subcategory.category_id == category_id
        )).first()


subcategory = SubcategoryCRUD(Subcategory)
