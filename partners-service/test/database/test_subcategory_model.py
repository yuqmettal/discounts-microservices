from sqlalchemy.orm import Session

from database import crud
from database.schema.subcategory_schema import SubcategoryCreate, SubcategoryUpdate
from test.util.subcategory_util import insert_subcategory, delete_subcategory


def test_list_all_subcategories(db: Session) -> None:
    subcategory_count = crud.subcategory.count(db)
    subcategories = crud.subcategory.filter(db)
    assert len(subcategories) == subcategory_count
    created = insert_subcategory(db)
    subcategories = crud.subcategory.filter(db)
    assert len(subcategories) == subcategory_count + 1
    delete_subcategory(db, created)


def test_create_subcategory(db: Session) -> None:
    created = insert_subcategory(db)
    subcategory_created = crud.subcategory.get_by_id(db, created.id)
    assert created.id == subcategory_created.id
    assert created.description == subcategory_created.description
    delete_subcategory(db, created)


def test_update_subcategory(db: Session) -> None:
    created = insert_subcategory(db)
    subcategory_from_db = crud.subcategory.get_by_id(db, created.id)
    subcategory_update = SubcategoryUpdate(name="Changed")
    updated_subcategory = crud.subcategory.update(
        db, db_object=subcategory_from_db, object_to_update=subcategory_update)
    subcategory_from_db = crud.subcategory.get_by_id(db, created.id)
    assert subcategory_from_db.id == updated_subcategory.id
    assert subcategory_from_db.name == "Changed"
    delete_subcategory(db, created)


def test_delete_subcategory(db: Session) -> None:
    created = insert_subcategory(db)

    subcategory_from_db = crud.subcategory.get_by_id(db, created.id)
    assert subcategory_from_db
    deleted = crud.subcategory.remove(db, id=created.id)
    subcategory_from_db = crud.subcategory.get_by_id(db, created.id)
    assert subcategory_from_db is None
    assert deleted.id == created.id
