from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.city_schema import City, CityCreate, CityUpdate
from test.util.city_util import insert_city, delete_city, create_random_city_data
from test.util.province_util import insert_province
from test.util.utils import random_upper_string


client = TestClient(app)


def test_GET_cities(db: Session) -> None:
    city_count = crud.city.count(db)
    response = client.get('/api/v1/city/')
    assert response.status_code == 200
    assert len(response.json()) == city_count
    created = insert_city(db)

    response = client.get('/api/v1/city/')
    assert response.status_code == 200
    assert len(response.json()) == city_count + 1
    
    delete_city(db, created)


def test_POST_new_city(db: Session) -> None:
    created_province = insert_province(db)
    city_data = create_random_city_data(created_province.id)
    response = client.post('/api/v1/city/', json=city_data)

    assert response.status_code == 200

    created_city = response.json()
    city_id = created_city.get("id")

    city_from_db = crud.city.get_by_id(db, city_id)

    assert city_from_db
    assert city_from_db.name == city_data['name']
    
    delete_city(db, city_from_db)


def test_POST_existing_city_name(db: Session) -> None:
    created = insert_city(db)

    city_data = {
        'name': created.name,
        'province_id': created.province_id,
    }
    response = client.post('/api/v1/city/', json=city_data)

    created_city = response.json()
    assert response.status_code == 400
    assert "_id" not in response

    delete_city(db, created)


def test_GET_existing_city(db: Session) -> None:
    created = insert_city(db)

    response = client.get(f'/api/v1/city/{created.id}')
    city_from_api = response.json()
    assert response.status_code == 200
    assert city_from_api['name'] == created.name
    
    delete_city(db, created)


def test_GET_unexisting_city(db: Session) -> None:
    response = client.get('/api/v1/city/0')
    created_city = response.json()
    assert response.status_code == 404
    assert "_id" not in created_city


def test_PUT_existing_city(db: Session) -> None:
    created = insert_city(db)

    city_data = {'name': 'Changed'}

    response = client.put(f'/api/v1/city/{created.id}', json=city_data)
    city_from_api = response.json()
    assert response.status_code == 200
    assert city_from_api['name'] == 'Changed'
    
    delete_city(db, created)


def test_PUT_unexisting_city(db: Session) -> None:
    city_data = {'name': 'Changed'}

    response = client.put('/api/v1/city/0', json=city_data)
    city_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in city_from_api


def test_DELETE_existing_city(db: Session) -> None:
    created = insert_city(db)

    response = client.delete(f'/api/v1/city/{created.id}')
    city_from_api = response.json()
    assert response.status_code == 200
    assert created.name == city_from_api['name']
    
    delete_city(db, created)


def test_DELETE_unexisting_city(db: Session) -> None:
    response = client.delete('/api/v1/city/0')
    city_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in city_from_api
