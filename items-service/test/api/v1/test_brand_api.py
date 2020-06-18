from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from app.database import crud
from app.database.schema.brand_schema import Brand, BrandCreate, BrandUpdate
from test.util.utils import random_upper_string
from test.util.brand_util import insert_brand, delete_brand, create_random_brand_data


client = TestClient(app)


def test_GET_brand(db: Session) -> None:
    brand_count = crud.brand.count(db)
    response = client.get('/api/v1/brand/')
    assert response.status_code == 200
    assert len(response.json()) == brand_count
    created = insert_brand(db)

    response = client.get('/api/v1/brand/')
    assert response.status_code == 200
    assert len(response.json()) == brand_count + 1
    
    delete_brand(db, created)


def test_POST_new_brand(db: Session) -> None:
    brand_data = create_random_brand_data()
    response = client.post('/api/v1/brand/', json=brand_data)

    assert response.status_code == 200

    created_brand = response.json()
    brand_id = created_brand.get("id")

    brand_from_db = crud.brand.get_by_id(db, brand_id)

    assert brand_from_db
    assert brand_from_db.name == brand_data['name']
    
    delete_brand(db, brand_from_db)


def test_POST_existing_brand_name(db: Session) -> None:
    created = insert_brand(db)

    brand_data = {
        'name': created.name,
    }
    response = client.post('/api/v1/brand/', json=brand_data)

    created_brand = response.json()
    assert response.status_code == 400
    assert "_id" not in created_brand

    delete_brand(db, created)


def test_GET_existing_brand(db: Session) -> None:
    created = insert_brand(db)

    response = client.get(f'/api/v1/brand/{created.id}')
    brand_from_api = response.json()
    assert response.status_code == 200
    assert brand_from_api['name'] == created.name
    
    delete_brand(db, created)


def test_GET_unexisting_brand(db: Session) -> None:
    response = client.get('/api/v1/brand/0')
    created_brand = response.json()
    assert response.status_code == 404
    assert "_id" not in created_brand


def test_PUT_existing_brand(db: Session) -> None:
    created = insert_brand(db)

    brand_data = {'name': 'Changed'}

    response = client.put(f'/api/v1/brand/{created.id}', json=brand_data)
    brand_from_api = response.json()
    assert response.status_code == 200
    assert brand_from_api['name'] == 'Changed'
    
    delete_brand(db, created)


def test_PUT_unexisting_brand(db: Session) -> None:
    brand_data = {'name': 'Changed'}

    response = client.put('/api/v1/brand/0', json=brand_data)
    brand_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in brand_from_api


def test_DELETE_existing_brand(db: Session) -> None:
    created = insert_brand(db)

    response = client.delete(f'/api/v1/brand/{created.id}')
    brand_from_api = response.json()
    assert response.status_code == 200
    assert created.name == brand_from_api['name']
    
    delete_brand(db, created)


def test_DELETE_unexisting_brand(db: Session) -> None:
    response = client.delete('/api/v1/brand/0')
    brand_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in brand_from_api
