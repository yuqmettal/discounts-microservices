from sqlalchemy.orm import Session

from database import crud
from database.schema.category_schema import CategoryCreate, CategoryUpdate
from test.util.category_util import insert_category, delete_category


def test_list_all_categories(db: Session) -> None:
    category_count = crud.category.count(db)
    categories = crud.category.filter(db)
    assert len(categories) == category_count
    created = insert_category(db)
    categories = crud.category.filter(db)
    assert len(categories) == category_count + 1
    delete_category(db, created)


def test_create_category(db: Session) -> None:
    created = insert_category(db)
    category_created = crud.category.get_by_id(db, created.id)
    assert created.id == category_created.id
    assert created.description == category_created.description
    delete_category(db, created)


def test_update_category(db: Session) -> None:
    created = insert_category(db)
    category_from_db = crud.category.get_by_id(db, created.id)
    category_update = CategoryUpdate(name="Changed")
    updated_category = crud.category.update(
        db, db_object=category_from_db, object_to_update=category_update)
    category_from_db = crud.category.get_by_id(db, created.id)
    assert category_from_db.id == updated_category.id
    assert category_from_db.name == "Changed"
    delete_category(db, created)


def test_delete_category(db: Session) -> None:
    created = insert_category(db)

    category_from_db = crud.category.get_by_id(db, created.id)
    assert category_from_db
    deleted = crud.category.remove(db, id=created.id)
    category_from_db = crud.category.get_by_id(db, created.id)
    assert category_from_db is None
    assert deleted.id == created.id
