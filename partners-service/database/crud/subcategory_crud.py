from typing import List

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

    def get_category_ids_from_subcategories(self, db: Session, *, subcategories: List[int]):
        categories_ids = db.query(Subcategory.category_id) \
            .filter(Subcategory.id.in_(subcategories)) \
            .distinct() \
            .all()
        return [x[0] for x in categories_ids]


subcategory = SubcategoryCRUD(Subcategory)
