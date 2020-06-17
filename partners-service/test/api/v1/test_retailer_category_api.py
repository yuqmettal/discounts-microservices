from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.retailer_category_schema import RetailerCategory, RetailerCategoryCreate, RetailerCategoryUpdate
from test.util.utils import random_upper_string
from test.util.retailer_category_util import insert_retailer_category, delete_retailer_category, create_random_retailer_category_data


client = TestClient(app)


def test_GET_retailer_category(db: Session) -> None:
    retailer_category_count = crud.retailer_category.count(db)
    response = client.get('/api/v1/retailer_category/')
    assert response.status_code == 200
    assert len(response.json()) == retailer_category_count
    created = insert_retailer_category(db)

    response = client.get('/api/v1/retailer_category/')
    assert response.status_code == 200
    assert len(response.json()) == retailer_category_count + 1

    delete_retailer_category(db, created)


def test_POST_new_retailer_category_valid_category_id(db: Session, mocker) -> None:
    retailer_category_data = create_random_retailer_category_data()
    response = client.post('/api/v1/retailer_category/', json=retailer_category_data)

    assert response.status_code == 200

    created_retailer_category = response.json()
    retailer_category_id = created_retailer_category.get("id")

    retailer_category_from_db = crud.retailer_category.get_by_id(db, retailer_category_id)

    assert retailer_category_from_db
    assert retailer_category_from_db.retailer_id == retailer_category_data['retailer_id']

    delete_retailer_category(db, retailer_category_from_db)


def test_GET_existing_retailer_category(db: Session) -> None:
    created = insert_retailer_category(db)

    response = client.get(f'/api/v1/retailer_category/{created.id}')
    retailer_category_from_api = response.json()
    assert response.status_code == 200
    assert retailer_category_from_api['retailer_id'] == created.retailer_id

    delete_retailer_category(db, created)


def test_GET_unexisting_retailer_category(db: Session) -> None:
    response = client.get('/api/v1/retailer_category/0')
    created_retailer_category = response.json()
    assert response.status_code == 404
    assert "_id" not in created_retailer_category


def test_PUT_existing_retailer_category(db: Session) -> None:
    created = insert_retailer_category(db)

    retailer_category_data = {'enabled': False}

    response = client.put(f'/api/v1/retailer_category/{created.id}', json=retailer_category_data)
    retailer_category_from_api = response.json()
    assert response.status_code == 200
    assert retailer_category_from_api['enabled'] == False

    delete_retailer_category(db, created)


def test_PUT_unexisting_retailer_category(db: Session) -> None:
    retailer_category_data = {'enabled': False}

    response = client.put('/api/v1/retailer_category/0', json=retailer_category_data)
    retailer_category_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in retailer_category_from_api


def test_DELETE_existing_retailer_category(db: Session) -> None:
    created = insert_retailer_category(db)

    response = client.delete(f'/api/v1/retailer_category/{created.id}')
    retailer_category_from_api = response.json()
    assert response.status_code == 200
    assert created.retailer_id == retailer_category_from_api['retailer_id']

    delete_retailer_category(db, created)


def test_DELETE_unexisting_retailer_category(db: Session) -> None:
    response = client.delete('/api/v1/retailer_category/0')
    retailer_category_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in retailer_category_from_api
