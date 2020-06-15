from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.subcategory_schema import Subcategory, SubcategoryCreate, SubcategoryUpdate
from test.util.utils import random_upper_string
from test.util.subcategory_util import insert_subcategory, delete_subcategory, create_random_subcategory_data


client = TestClient(app)


def test_GET_subcategory(db: Session) -> None:
    subcategory_count = crud.subcategory.count(db)
    response = client.get('/api/v1/subcategory/')
    assert response.status_code == 200
    assert len(response.json()) == subcategory_count
    created = insert_subcategory(db)

    response = client.get('/api/v1/subcategory/')
    assert response.status_code == 200
    assert len(response.json()) == subcategory_count + 1
    
    delete_subcategory(db, created)


def test_POST_new_subcategory(db: Session) -> None:
    subcategory_data = create_random_subcategory_data()
    response = client.post('/api/v1/subcategory/', json=subcategory_data)

    assert response.status_code == 200

    created_subcategory = response.json()
    subcategory_id = created_subcategory.get("id")

    subcategory_from_db = crud.subcategory.get_by_id(db, subcategory_id)

    assert subcategory_from_db
    assert subcategory_from_db.name == subcategory_data['name']
    
    delete_subcategory(db, subcategory_from_db)


def test_POST_existing_subcategory_name(db: Session) -> None:
    created = insert_subcategory(db)

    subcategory_data = {
        'name': created.name,
        'description': random_upper_string(),
        'category_id': 1
    }
    response = client.post('/api/v1/subcategory/', json=subcategory_data)

    created_subcategory = response.json()
    assert response.status_code == 400
    assert "_id" not in created_subcategory

    delete_subcategory(db, created)


def test_GET_existing_subcategory(db: Session) -> None:
    created = insert_subcategory(db)

    response = client.get(f'/api/v1/subcategory/{created.id}')
    subcategory_from_api = response.json()
    assert response.status_code == 200
    assert subcategory_from_api['name'] == created.name
    
    delete_subcategory(db, created)


def test_GET_unexisting_subcategory(db: Session) -> None:
    response = client.get('/api/v1/subcategory/0')
    created_subcategory = response.json()
    assert response.status_code == 404
    assert "_id" not in created_subcategory


def test_PUT_existing_subcategory(db: Session) -> None:
    created = insert_subcategory(db)

    subcategory_data = {'name': 'Changed'}

    response = client.put(f'/api/v1/subcategory/{created.id}', json=subcategory_data)
    subcategory_from_api = response.json()
    assert response.status_code == 200
    assert subcategory_from_api['name'] == 'Changed'
    
    delete_subcategory(db, created)


def test_PUT_unexisting_subcategory(db: Session) -> None:
    subcategory_data = {'name': 'Changed'}

    response = client.put('/api/v1/subcategory/0', json=subcategory_data)
    subcategory_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in subcategory_from_api


def test_DELETE_existing_subcategory(db: Session) -> None:
    created = insert_subcategory(db)

    response = client.delete(f'/api/v1/subcategory/{created.id}')
    subcategory_from_api = response.json()
    assert response.status_code == 200
    assert created.name == subcategory_from_api['name']
    
    delete_subcategory(db, created)


def test_DELETE_unexisting_subcategory(db: Session) -> None:
    response = client.delete('/api/v1/subcategory/0')
    subcategory_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in subcategory_from_api