from sqlalchemy.orm import Session

from database import crud
from database.schema.cart_item_schema import CartItemCreate, CartItemUpdate
from test.util.cart_item_util import insert_cart_item, delete_cart_item


def test_list_all_cart_items(db: Session) -> None:
    cart_item_count = crud.cart_item.count(db)
    cart_items = crud.cart_item.filter(db)
    assert len(cart_items) == cart_item_count
    created = insert_cart_item(db)
    cart_items = crud.cart_item.filter(db)
    assert len(cart_items) == cart_item_count + 1
    delete_cart_item(db, created)


def test_create_cart_item(db: Session) -> None:
    created = insert_cart_item(db)
    cart_item_created = crud.cart_item.get_by_id(db, created.id)
    assert created.id == cart_item_created.id
    assert created.item_id == cart_item_created.item_id
    delete_cart_item(db, created)


def test_update_cart_item(db: Session) -> None:
    created = insert_cart_item(db)
    cart_item_from_db = crud.cart_item.get_by_id(db, created.id)
    cart_item_update = CartItemUpdate(item_id=8)
    updated_cart_item = crud.cart_item.update(
        db, db_object=cart_item_from_db, object_to_update=cart_item_update)
    cart_item_from_db = crud.cart_item.get_by_id(db, created.id)
    assert cart_item_from_db.id == updated_cart_item.id
    assert cart_item_from_db.item_id == 8
    delete_cart_item(db, created)


def test_delete_cart_item(db: Session) -> None:
    created = insert_cart_item(db)

    cart_item_from_db = crud.cart_item.get_by_id(db, created.id)
    assert cart_item_from_db
    deleted = crud.cart_item.remove(db, id=created.id)
    cart_item_from_db = crud.cart_item.get_by_id(db, created.id)
    assert cart_item_from_db is None
    assert deleted.id == created.id
