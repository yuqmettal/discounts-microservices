from sqlalchemy.orm import Session

from database import crud
from database.schema.client_cart_schema import ClientCartCreate, ClientCartUpdate
from test.util.client_cart_util import insert_client_cart, delete_client_cart


def test_list_all_client_carts(db: Session) -> None:
    client_cart_count = crud.client_cart.count(db)
    client_carts = crud.client_cart.filter(db)
    assert len(client_carts) == client_cart_count
    created = insert_client_cart(db)
    client_carts = crud.client_cart.filter(db)
    assert len(client_carts) == client_cart_count + 1
    delete_client_cart(db, created)


def test_create_client_cart(db: Session) -> None:
    created = insert_client_cart(db)
    client_cart_created = crud.client_cart.get_by_id(db, created.id)
    assert created.id == client_cart_created.id
    assert created.client_id == client_cart_created.client_id
    delete_client_cart(db, created)


def test_update_client_cart(db: Session) -> None:
    created = insert_client_cart(db)
    client_cart_from_db = crud.client_cart.get_by_id(db, created.id)
    client_cart_update = ClientCartUpdate(client_id=8)
    updated_client_cart = crud.client_cart.update(
        db, db_object=client_cart_from_db, object_to_update=client_cart_update)
    client_cart_from_db = crud.client_cart.get_by_id(db, created.id)
    assert client_cart_from_db.id == updated_client_cart.id
    assert client_cart_from_db.client_id == 8
    delete_client_cart(db, created)


def test_delete_client_cart(db: Session) -> None:
    created = insert_client_cart(db)

    client_cart_from_db = crud.client_cart.get_by_id(db, created.id)
    assert client_cart_from_db
    deleted = crud.client_cart.remove(db, id=created.id)
    client_cart_from_db = crud.client_cart.get_by_id(db, created.id)
    assert client_cart_from_db is None
    assert deleted.id == created.id
