from sqlalchemy.orm import Session

from database import crud
from database.schema.cart_schema import CartCreate, CartUpdate
from test.util.cart_util import insert_cart, delete_cart


def test_list_all_carts(db: Session) -> None:
    cart_count = crud.cart.count(db)
    carts = crud.cart.filter(db)
    assert len(carts) == cart_count
    created = insert_cart(db)
    carts = crud.cart.filter(db)
    assert len(carts) == cart_count + 1
    delete_cart(db, created)


def test_create_cart(db: Session) -> None:
    created = insert_cart(db)
    cart_created = crud.cart.get_by_id(db, created.id)
    assert created.id == cart_created.id
    assert created.name == cart_created.name
    delete_cart(db, created)


def test_update_cart(db: Session) -> None:
    created = insert_cart(db)
    cart_from_db = crud.cart.get_by_id(db, created.id)
    cart_update = CartUpdate(name="Changed")
    updated_cart = crud.cart.update(
        db, db_object=cart_from_db, object_to_update=cart_update)
    cart_from_db = crud.cart.get_by_id(db, created.id)
    assert cart_from_db.id == updated_cart.id
    assert cart_from_db.name == "Changed"
    delete_cart(db, created)


def test_delete_cart(db: Session) -> None:
    created = insert_cart(db)

    cart_from_db = crud.cart.get_by_id(db, created.id)
    assert cart_from_db
    deleted = crud.cart.remove(db, id=created.id)
    cart_from_db = crud.cart.get_by_id(db, created.id)
    assert cart_from_db is None
    assert deleted.id == created.id
