from sqlalchemy.orm import Session

from database import crud
from database.schema.order_item_schema import OrderItemCreate, OrderItemUpdate
from test.util.order_item_util import insert_order_item, delete_order_item


def test_list_all_order_items(db: Session) -> None:
    order_item_count = crud.order_item.count(db)
    order_items = crud.order_item.filter(db)
    assert len(order_items) == order_item_count
    created = insert_order_item(db)
    order_items = crud.order_item.filter(db)
    assert len(order_items) == order_item_count + 1
    delete_order_item(db, created)


def test_create_order_item(db: Session) -> None:
    created = insert_order_item(db)
    order_item_created = crud.order_item.get_by_id(db, created.id)
    assert created.id == order_item_created.id
    assert created.item_id == order_item_created.item_id
    delete_order_item(db, created)


def test_update_order_item(db: Session) -> None:
    created = insert_order_item(db)
    order_item_from_db = crud.order_item.get_by_id(db, created.id)
    order_item_update = OrderItemUpdate(item_id=8)
    updated_order_item = crud.order_item.update(
        db, db_object=order_item_from_db, object_to_update=order_item_update)
    order_item_from_db = crud.order_item.get_by_id(db, created.id)
    assert order_item_from_db.id == updated_order_item.id
    assert order_item_from_db.item_id == 8
    delete_order_item(db, created)


def test_delete_order_item(db: Session) -> None:
    created = insert_order_item(db)

    order_item_from_db = crud.order_item.get_by_id(db, created.id)
    assert order_item_from_db
    deleted = crud.order_item.remove(db, id=created.id)
    order_item_from_db = crud.order_item.get_by_id(db, created.id)
    assert order_item_from_db is None
    assert deleted.id == created.id
