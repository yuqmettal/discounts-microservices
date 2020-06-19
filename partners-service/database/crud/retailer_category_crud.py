from typing import List

from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import RetailerCategory
from database.schema.retailer_category_schema import RetailerCategoryCreate, RetailerCategoryUpdate


class RetailerCategoryCRUD(CRUDBase[RetailerCategory, RetailerCategoryCreate, RetailerCategoryUpdate]):
    def get_by_categories(self, db: Session, *, categories: List[int]):
        return db.query(RetailerCategory.retailer_id) \
            .filter(RetailerCategory.category_id.in_(categories)) \
            .distinct() \
            .all()


retailer_category = RetailerCategoryCRUD(RetailerCategory)
