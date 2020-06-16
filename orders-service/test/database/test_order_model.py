from sqlalchemy.orm import Session

from database import crud
from database.schema.order_schema import OrderCreate, OrderUpdate
from test.util.order_util import insert_order, delete_order


def test_list_all_orders(db: Session) -> None:
    order_count = crud.order.count(db)
    orders = crud.order.filter(db)
    assert len(orders) == order_count
    created = insert_order(db)
    orders = crud.order.filter(db)
    assert len(orders) == order_count + 1
    delete_order(db, created)


def test_create_order(db: Session) -> None:
    created = insert_order(db)
    order_created = crud.order.get_by_id(db, created.id)
    assert created.id == order_created.id
    assert created.address_id == order_created.address_id
    delete_order(db, created)


def test_update_order(db: Session) -> None:
    created = insert_order(db)
    order_from_db = crud.order.get_by_id(db, created.id)
    order_update = OrderUpdate(address_id=8)
    updated_order = crud.order.update(
        db, db_object=order_from_db, object_to_update=order_update)
    order_from_db = crud.order.get_by_id(db, created.id)
    assert order_from_db.id == updated_order.id
    assert order_from_db.address_id == 8
    delete_order(db, created)


def test_delete_order(db: Session) -> None:
    created = insert_order(db)

    order_from_db = crud.order.get_by_id(db, created.id)
    assert order_from_db
    deleted = crud.order.remove(db, id=created.id)
    order_from_db = crud.order.get_by_id(db, created.id)
    assert order_from_db is None
    assert deleted.id == created.id
