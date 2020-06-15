from sqlalchemy.orm import Session

from database import crud
from database.schema.retailer_schema import RetailerCreate, RetailerUpdate
from test.util.retailer_util import insert_retailer, delete_retailer


def test_list_all_retailers(db: Session) -> None:
    retailer_count = crud.retailer.count(db)
    retailers = crud.retailer.filter(db)
    assert len(retailers) == retailer_count
    created = insert_retailer(db)
    retailers = crud.retailer.filter(db)
    assert len(retailers) == retailer_count + 1
    delete_retailer(db, created)


def test_create_retailer(db: Session) -> None:
    created = insert_retailer(db)
    retailer_created = crud.retailer.get_by_id(db, created.id)
    assert created.id == retailer_created.id
    assert created.description == retailer_created.description
    delete_retailer(db, created)


def test_update_retailer(db: Session) -> None:
    created = insert_retailer(db)
    retailer_from_db = crud.retailer.get_by_id(db, created.id)
    retailer_update = RetailerUpdate(name="Changed")
    updated_retailer = crud.retailer.update(
        db, db_object=retailer_from_db, object_to_update=retailer_update)
    retailer_from_db = crud.retailer.get_by_id(db, created.id)
    assert retailer_from_db.id == updated_retailer.id
    assert retailer_from_db.name == "Changed"
    delete_retailer(db, created)


def test_delete_retailer(db: Session) -> None:
    created = insert_retailer(db)

    retailer_from_db = crud.retailer.get_by_id(db, created.id)
    assert retailer_from_db
    deleted = crud.retailer.remove(db, id=created.id)
    retailer_from_db = crud.retailer.get_by_id(db, created.id)
    assert retailer_from_db is None
    assert deleted.id == created.id
