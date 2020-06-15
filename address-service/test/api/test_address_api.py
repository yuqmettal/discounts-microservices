from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.address_schema import Address, AddressCreate, AddressUpdate
from test.util.utils import random_upper_string
from test.util.address_util import insert_address, delete_address, insert_city, create_random_address_data


client = TestClient(app)


def test_GET_address(db: Session) -> None:
    address_count = crud.address.count(db)
    response = client.get('/api/v1/address/')
    assert response.status_code == 200
    assert len(response.json()) == address_count
    created = insert_address(db)

    response = client.get('/api/v1/address/')
    assert response.status_code == 200
    assert len(response.json()) == address_count + 1
    
    delete_address(db, created)


def test_POST_new_address(db: Session) -> None:
    address_data = create_random_address_data()
    response = client.post('/api/v1/address/', json=address_data)

    assert response.status_code == 200

    created_address = response.json()
    address_id = created_address.get("id")

    address_from_db = crud.address.get_by_id(db, address_id)

    assert address_from_db
    assert address_from_db.name == address_data['name']
    
    delete_address(db, address_from_db)


def test_GET_existing_address(db: Session) -> None:
    created = insert_address(db)

    response = client.get(f'/api/v1/address/{created.id}')
    address_from_api = response.json()
    assert response.status_code == 200
    assert address_from_api['name'] == created.name
    
    delete_address(db, created)


def test_GET_unexisting_address(db: Session) -> None:
    response = client.get('/api/v1/address/0')
    created_address = response.json()
    assert response.status_code == 404
    assert "_id" not in created_address


def test_PUT_existing_address(db: Session) -> None:
    created = insert_address(db)

    address_data = {'name': 'Changed'}

    response = client.put(f'/api/v1/address/{created.id}', json=address_data)
    address_from_api = response.json()
    assert response.status_code == 200
    assert address_from_api['name'] == 'Changed'
    
    delete_address(db, created)


def test_PUT_unexisting_address(db: Session) -> None:
    address_data = {'name': 'Changed'}

    response = client.put('/api/v1/address/0', json=address_data)
    address_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in address_from_api


def test_DELETE_existing_address(db: Session) -> None:
    created = insert_address(db)

    response = client.delete(f'/api/v1/address/{created.id}')
    address_from_api = response.json()
    assert response.status_code == 200
    assert created.name == address_from_api['name']
    
    delete_address(db, created)


def test_DELETE_unexisting_address(db: Session) -> None:
    response = client.delete('/api/v1/address/0')
    address_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in address_from_api
