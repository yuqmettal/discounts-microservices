from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.retailer_sector_schema import RetailerSector, RetailerSectorCreate, RetailerSectorUpdate
from test.util.utils import random_upper_string
from test.util.retailer_sector_util import insert_retailer_sector, delete_retailer_sector, create_random_retailer_sector_data
from client.base import EurekaResponse


client = TestClient(app)


def test_GET_retailer_sector(db: Session) -> None:
    retailer_sector_count = crud.retailer_sector.count(db)
    response = client.get('/api/v1/retailer_sector/')
    assert response.status_code == 200
    assert len(response.json()) == retailer_sector_count
    created = insert_retailer_sector(db)

    response = client.get('/api/v1/retailer_sector/')
    assert response.status_code == 200
    assert len(response.json()) == retailer_sector_count + 1

    delete_retailer_sector(db, created)


def test_POST_new_retailer_sector_valid_sector_id(db: Session, mocker) -> None:
    sector_response = EurekaResponse(
        200, {'name': 'mocked', 'city_id': 1, 'id': 1})
    mocker.patch(
        'client.address_client._address_client.call_remote_service',
        return_value=sector_response
    )

    retailer_sector_data = create_random_retailer_sector_data()
    response = client.post('/api/v1/retailer_sector/', json=retailer_sector_data)

    assert response.status_code == 200

    created_retailer_sector = response.json()
    retailer_sector_id = created_retailer_sector.get("id")

    retailer_sector_from_db = crud.retailer_sector.get_by_id(db, retailer_sector_id)

    assert retailer_sector_from_db
    assert retailer_sector_from_db.retailer_id == retailer_sector_data['retailer_id']

    delete_retailer_sector(db, retailer_sector_from_db)


def test_POST_new_retailer_sector_invalid_city_id(db: Session, mocker) -> None:
    city_response = EurekaResponse(
        404, {'name': 'mocked', 'province_id': 1, 'id': 1})
    mocker.patch(
        'client.address_client._address_client.call_remote_service',
        return_value=city_response
    )

    retailer_sector_data = create_random_retailer_sector_data()
    response = client.post('/api/v1/retailer_sector/', json=retailer_sector_data)

    created_retailer_sector = response.json()
    assert response.status_code == 400
    assert "_id" not in created_retailer_sector


def test_GET_existing_retailer_sector(db: Session) -> None:
    created = insert_retailer_sector(db)

    response = client.get(f'/api/v1/retailer_sector/{created.id}')
    retailer_sector_from_api = response.json()
    assert response.status_code == 200
    assert retailer_sector_from_api['retailer_id'] == created.retailer_id

    delete_retailer_sector(db, created)


def test_GET_unexisting_retailer_sector(db: Session) -> None:
    response = client.get('/api/v1/retailer_sector/0')
    created_retailer_sector = response.json()
    assert response.status_code == 404
    assert "_id" not in created_retailer_sector


def test_PUT_existing_retailer_sector(db: Session) -> None:
    created = insert_retailer_sector(db)

    retailer_sector_data = {'enabled': False}

    response = client.put(f'/api/v1/retailer_sector/{created.id}', json=retailer_sector_data)
    retailer_sector_from_api = response.json()
    assert response.status_code == 200
    assert retailer_sector_from_api['enabled'] == False

    delete_retailer_sector(db, created)


def test_PUT_unexisting_retailer_sector(db: Session) -> None:
    retailer_sector_data = {'enabled': False}

    response = client.put('/api/v1/retailer_sector/0', json=retailer_sector_data)
    retailer_sector_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in retailer_sector_from_api


def test_DELETE_existing_retailer_sector(db: Session) -> None:
    created = insert_retailer_sector(db)

    response = client.delete(f'/api/v1/retailer_sector/{created.id}')
    retailer_sector_from_api = response.json()
    assert response.status_code == 200
    assert created.retailer_id == retailer_sector_from_api['retailer_id']

    delete_retailer_sector(db, created)


def test_DELETE_unexisting_retailer_sector(db: Session) -> None:
    response = client.delete('/api/v1/retailer_sector/0')
    retailer_sector_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in retailer_sector_from_api
