from sqlalchemy.orm import Session

from database import crud
from database.schema.client_schema import ClientCreate, ClientUpdate
from test.util.client_util import insert_client, delete_client


def test_list_all_clients(db: Session) -> None:
    client_count = crud.client.count(db)
    clients = crud.client.filter(db)
    assert len(clients) == client_count
    created = insert_client(db)
    clients = crud.client.filter(db)
    assert len(clients) == client_count + 1
    delete_client(db, created)


def test_create_client(db: Session) -> None:
    created = insert_client(db)
    client_created = crud.client.get_by_id(db, created.id)
    assert created.id == client_created.id
    assert created.email == client_created.email
    delete_client(db, created)


def test_update_client(db: Session) -> None:
    created = insert_client(db)
    client_from_db = crud.client.get_by_id(db, created.id)
    client_update = ClientUpdate(name="Changed")
    updated_client = crud.client.update(
        db, db_object=client_from_db, object_to_update=client_update)
    client_from_db = crud.client.get_by_id(db, created.id)
    assert client_from_db.id == updated_client.id
    assert client_from_db.name == "Changed"
    delete_client(db, created)


def test_delete_client(db: Session) -> None:
    created = insert_client(db)

    client_from_db = crud.client.get_by_id(db, created.id)
    assert client_from_db
    deleted = crud.client.remove(db, id=created.id)
    client_from_db = crud.client.get_by_id(db, created.id)
    assert client_from_db is None
    assert deleted.id == created.id
