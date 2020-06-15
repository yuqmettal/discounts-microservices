from sqlalchemy.orm import Session

from database import crud
from database.schema.address_schema import AddressCreate, AddressUpdate
from database import models
from test.util.address_util import insert_address, delete_address


def test_list_all_addresses(db: Session) -> None:
    address_count = crud.address.count(db)
    addresses = crud.address.filter(db)
    assert len(addresses) == address_count

    created = insert_address(db)
    addresses = crud.address.filter(db)
    assert len(addresses) == address_count + 1

    delete_address(db, created)


def test_create_address(db: Session) -> None:
    created = insert_address(db)
    address_created = crud.address.get_by_id(db, created.id)
    assert created.id == address_created.id
    assert created.name == address_created.name

    delete_address(db, created)


def test_update_address(db: Session) -> None:
    created = insert_address(db)
    address_from_db = crud.address.get_by_id(db, created.id)
    address_update = AddressUpdate(name="Updated")
    updated_address = crud.address.update(
        db, db_object=address_from_db, object_to_update=address_update)
    address_from_db = crud.address.get_by_id(db, created.id)
    assert address_from_db.id == updated_address.id
    assert address_from_db.name == "Updated"

    delete_address(db, created)


def test_delete_address(db: Session) -> None:
    created = insert_address(db)
    address_from_db = crud.address.get_by_id(db, created.id)
    assert address_from_db
    deleted = crud.address.remove(db, id=created.id)
    address_from_db = crud.address.get_by_id(db, created.id)
    assert address_from_db is None
    assert deleted.id == created.id
