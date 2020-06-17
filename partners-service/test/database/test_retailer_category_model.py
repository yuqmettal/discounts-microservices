from sqlalchemy.orm import Session

from database import crud
from database.schema.retailer_category_schema import RetailerCategoryCreate, RetailerCategoryUpdate
from test.util.retailer_category_util import insert_retailer_category, delete_retailer_category


def test_list_all_retailer_categories(db: Session) -> None:
    retailer_category_count = crud.retailer_category.count(db)
    retailer_categories = crud.retailer_category.filter(db)
    assert len(retailer_categories) == retailer_category_count
    created = insert_retailer_category(db)
    retailer_categories = crud.retailer_category.filter(db)
    assert len(retailer_categories) == retailer_category_count + 1
    delete_retailer_category(db, created)


def test_create_retailer_category(db: Session) -> None:
    created = insert_retailer_category(db)
    retailer_category_created = crud.retailer_category.get_by_id(db, created.id)
    assert created.id == retailer_category_created.id
    assert created.retailer_id == retailer_category_created.retailer_id
    delete_retailer_category(db, created)


def test_update_retailer_category(db: Session) -> None:
    created = insert_retailer_category(db)
    retailer_category_from_db = crud.retailer_category.get_by_id(db, created.id)
    retailer_category_update = RetailerCategoryUpdate(enabled=False)
    updated_retailer_category = crud.retailer_category.update(
        db, db_object=retailer_category_from_db, object_to_update=retailer_category_update)
    retailer_category_from_db = crud.retailer_category.get_by_id(db, created.id)
    assert retailer_category_from_db.id == updated_retailer_category.id
    assert retailer_category_from_db.enabled == False
    delete_retailer_category(db, created)


def test_delete_retailer_category(db: Session) -> None:
    created = insert_retailer_category(db)

    retailer_category_from_db = crud.retailer_category.get_by_id(db, created.id)
    assert retailer_category_from_db
    deleted = crud.retailer_category.remove(db, id=created.id)
    retailer_category_from_db = crud.retailer_category.get_by_id(db, created.id)
    assert retailer_category_from_db is None
    assert deleted.id == created.id
