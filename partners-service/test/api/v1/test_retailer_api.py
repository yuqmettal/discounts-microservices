from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.retailer_schema import Retailer, RetailerCreate, RetailerUpdate
from test.util.utils import random_upper_string
from test.util.retailer_util import insert_retailer, delete_retailer, create_random_retailer_data
from client.base import EurekaResponse


client = TestClient(app)


def test_GET_retailer(db: Session) -> None:
    retailer_count = crud.retailer.count(db)
    response = client.get('/api/v1/retailer/')
    assert response.status_code == 200
    assert len(response.json()) == retailer_count
    created = insert_retailer(db)

    response = client.get('/api/v1/retailer/')
    assert response.status_code == 200
    assert len(response.json()) == retailer_count + 1

    delete_retailer(db, created)


def test_POST_new_retailer_valid_city_id(db: Session, mocker) -> None:
    city_response = EurekaResponse(
        200, {'name': 'mocked', 'province_id': 1, 'id': 1})
    mocker.patch(
        'client.address_client._address_client.call_remote_service',
        return_value=city_response
    )

    retailer_data = create_random_retailer_data()
    response = client.post('/api/v1/retailer/', json=retailer_data)

    assert response.status_code == 200

    created_retailer = response.json()
    retailer_id = created_retailer.get("id")

    retailer_from_db = crud.retailer.get_by_id(db, retailer_id)

    assert retailer_from_db
    assert retailer_from_db.name == retailer_data['name']

    delete_retailer(db, retailer_from_db)


def test_POST_new_retailer_invalid_city_id(db: Session, mocker) -> None:
    city_response = EurekaResponse(
        404, {'name': 'mocked', 'province_id': 1, 'id': 1})
    mocker.patch(
        'client.address_client._address_client.call_remote_service',
        return_value=city_response
    )

    retailer_data = create_random_retailer_data()
    response = client.post('/api/v1/retailer/', json=retailer_data)

    created_retailer = response.json()
    assert response.status_code == 400
    assert "_id" not in created_retailer


def test_POST_existing_retailer_name(db: Session) -> None:
    created = insert_retailer(db)

    retailer_data = {
        'name': created.name,
        'description': random_upper_string(),
        'city_id': 1
    }
    response = client.post('/api/v1/retailer/', json=retailer_data)

    created_retailer = response.json()
    assert response.status_code == 400
    assert "_id" not in created_retailer

    delete_retailer(db, created)


def test_GET_existing_retailer(db: Session) -> None:
    created = insert_retailer(db)

    response = client.get(f'/api/v1/retailer/{created.id}')
    retailer_from_api = response.json()
    assert response.status_code == 200
    assert retailer_from_api['name'] == created.name

    delete_retailer(db, created)


def test_GET_unexisting_retailer(db: Session) -> None:
    response = client.get('/api/v1/retailer/0')
    created_retailer = response.json()
    assert response.status_code == 404
    assert "_id" not in created_retailer


def test_PUT_existing_retailer(db: Session) -> None:
    created = insert_retailer(db)

    retailer_data = {'name': 'Changed'}

    response = client.put(f'/api/v1/retailer/{created.id}', json=retailer_data)
    retailer_from_api = response.json()
    assert response.status_code == 200
    assert retailer_from_api['name'] == 'Changed'

    delete_retailer(db, created)


def test_PUT_unexisting_retailer(db: Session) -> None:
    retailer_data = {'name': 'Changed'}

    response = client.put('/api/v1/retailer/0', json=retailer_data)
    retailer_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in retailer_from_api


def test_DELETE_existing_retailer(db: Session) -> None:
    created = insert_retailer(db)

    response = client.delete(f'/api/v1/retailer/{created.id}')
    retailer_from_api = response.json()
    assert response.status_code == 200
    assert created.name == retailer_from_api['name']

    delete_retailer(db, created)


def test_DELETE_unexisting_retailer(db: Session) -> None:
    response = client.delete('/api/v1/retailer/0')
    retailer_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in retailer_from_api
