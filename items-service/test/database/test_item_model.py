from sqlalchemy.orm import Session

from app.database import crud
from app.database.schema.item_schema import ItemCreate, ItemUpdate
from test.util.item_util import insert_item, delete_item


def test_list_all_items(db: Session) -> None:
    item_count = crud.item.count(db)
    items = crud.item.filter(db)
    assert len(items) == item_count
    created = insert_item(db)
    items = crud.item.filter(db)
    assert len(items) == item_count + 1
    delete_item(db, created)


def test_create_item(db: Session) -> None:
    created = insert_item(db)
    item_created = crud.item.get_by_id(db, created.id)
    assert created.id == item_created.id
    assert created.category_id == item_created.category_id
    delete_item(db, created)


def test_update_item(db: Session) -> None:
    created = insert_item(db)
    item_from_db = crud.item.get_by_id(db, created.id)
    item_update = ItemUpdate(retailer_id=8)
    updated_item = crud.item.update(
        db, db_object=item_from_db, object_to_update=item_update)
    item_from_db = crud.item.get_by_id(db, created.id)
    assert item_from_db.id == updated_item.id
    assert item_from_db.retailer_id == 8
    delete_item(db, created)


def test_delete_item(db: Session) -> None:
    created = insert_item(db)

    item_from_db = crud.item.get_by_id(db, created.id)
    assert item_from_db
    deleted = crud.item.remove(db, id=created.id)
    item_from_db = crud.item.get_by_id(db, created.id)
    assert item_from_db is None
    assert deleted.id == created.id
