from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import RetailerCategory
from database.schema.retailer_category_schema import RetailerCategoryCreate, RetailerCategoryUpdate


class RetailerCategoryCRUD(CRUDBase[RetailerCategory, RetailerCategoryCreate, RetailerCategoryUpdate]):
    pass


retailer_category = RetailerCategoryCRUD(RetailerCategory)
