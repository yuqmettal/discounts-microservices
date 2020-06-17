from sqlalchemy.orm import Session

from database.schema.retailer_category_schema import RetailerCategoryCreate
from database import crud
from database.models import RetailerCategory


def create_random_retailer_category() -> RetailerCategoryCreate:
    category_id = 1
    retailer_id = 1
    enabled = True
    return RetailerCategoryCreate(category_id=category_id, retailer_id=retailer_id, enabled=enabled)


def create_random_retailer_category_data():
    category_id = 1
    retailer_id = 1
    enabled = True
    return {'category_id': category_id, 'retailer_id': retailer_id, 'enabled': enabled}


def insert_retailer_category(db: Session):
    retailer_category_create = create_random_retailer_category()
    return crud.retailer_category.create(db, retailer_category_create)


def delete_retailer_category(db: Session, retailer_category: RetailerCategory):
    crud.retailer_category.remove(db, id=retailer_category.id)
