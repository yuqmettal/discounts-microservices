from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.category_schema import Category, CategoryCreate, CategoryUpdate
from test.util.utils import random_upper_string
from test.util.category_util import insert_category, delete_category, create_random_category_data


client = TestClient(app)


def test_GET_category(db: Session) -> None:
    category_count = crud.category.count(db)
    response = client.get('/api/v1/category/')
    assert response.status_code == 200
    assert len(response.json()) == category_count
    created = insert_category(db)

    response = client.get('/api/v1/category/')
    assert response.status_code == 200
    assert len(response.json()) == category_count + 1
    
    delete_category(db, created)


def test_POST_new_category(db: Session) -> None:
    category_data = create_random_category_data()
    response = client.post('/api/v1/category/', json=category_data)

    assert response.status_code == 200

    created_category = response.json()
    category_id = created_category.get("id")

    category_from_db = crud.category.get_by_id(db, category_id)

    assert category_from_db
    assert category_from_db.name == category_data['name']
    
    delete_category(db, category_from_db)


def test_POST_existing_category_name(db: Session) -> None:
    created = insert_category(db)

    category_data = {
        'name': created.name,
        'description': random_upper_string(),
    }
    response = client.post('/api/v1/category/', json=category_data)

    created_category = response.json()
    assert response.status_code == 400
    assert "_id" not in created_category

    delete_category(db, created)


def test_GET_existing_category(db: Session) -> None:
    created = insert_category(db)

    response = client.get(f'/api/v1/category/{created.id}')
    category_from_api = response.json()
    assert response.status_code == 200
    assert category_from_api['name'] == created.name
    
    delete_category(db, created)


def test_GET_unexisting_category(db: Session) -> None:
    response = client.get('/api/v1/category/0')
    created_category = response.json()
    assert response.status_code == 404
    assert "_id" not in created_category


def test_PUT_existing_category(db: Session) -> None:
    created = insert_category(db)

    category_data = {'name': 'Changed'}

    response = client.put(f'/api/v1/category/{created.id}', json=category_data)
    category_from_api = response.json()
    assert response.status_code == 200
    assert category_from_api['name'] == 'Changed'
    
    delete_category(db, created)


def test_PUT_unexisting_category(db: Session) -> None:
    category_data = {'name': 'Changed'}

    response = client.put('/api/v1/category/0', json=category_data)
    category_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in category_from_api


def test_DELETE_existing_category(db: Session) -> None:
    created = insert_category(db)

    response = client.delete(f'/api/v1/category/{created.id}')
    category_from_api = response.json()
    assert response.status_code == 200
    assert created.name == category_from_api['name']
    
    delete_category(db, created)


def test_DELETE_unexisting_category(db: Session) -> None:
    response = client.delete('/api/v1/category/0')
    category_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in category_from_api