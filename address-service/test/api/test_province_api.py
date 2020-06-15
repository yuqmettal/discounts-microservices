from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema import Province, ProvinceCreate, ProvinceUpdate
from test.util.country_util import insert_country
from test.util.province_util import insert_province, create_random_province_data
from test.util.utils import random_upper_string


client = TestClient(app)


def test_GET_provinces(db: Session) -> None:
    province_count = crud.province.count(db)
    response = client.get('/api/v1/province/')
    assert response.status_code == 200
    assert len(response.json()) == province_count
    created = insert_province(db)

    response = client.get('/api/v1/province/')
    assert response.status_code == 200
    assert len(response.json()) == province_count + 1
    crud.country.remove(db, id=created.country_id)
    crud.province.remove(db, id=created.id)


def test_POST_new_province(db: Session) -> None:
    created_country = insert_country(db)
    province_data = create_random_province_data(created_country.id)
    response = client.post('/api/v1/province/', json=province_data)

    assert response.status_code == 200

    created_province = response.json()
    province_id = created_province.get("id")

    province_from_db = crud.province.get_by_id(db, province_id)

    assert province_from_db
    assert province_from_db.name == province_data['name']
    
    crud.country.remove(db, id=province_from_db.country_id)
    crud.province.remove(db, id=province_from_db.id)


def test_POST_existing_province_name(db: Session) -> None:
    created = insert_province(db)

    province_data = {
        'name': created.name,
        'country_id': created.country_id,
        'region': random_upper_string(),
    }
    response = client.post('/api/v1/province/', json=province_data)

    created_country = response.json()
    assert response.status_code == 400
    assert "_id" not in response

    crud.province.remove(db, id=created.id)
    crud.country.remove(db, id=created.country_id)


def test_GET_existing_province(db: Session) -> None:
    created = insert_province(db)

    response = client.get(f'/api/v1/province/{created.id}')
    province_from_api = response.json()
    assert response.status_code == 200
    assert province_from_api['name'] == created.name
    crud.province.remove(db, id=created.id)
    crud.country.remove(db, id=created.country_id)


def test_GET_unexisting_province(db: Session) -> None:
    response = client.get('/api/v1/province/0')
    created_province = response.json()
    assert response.status_code == 404
    assert "_id" not in created_province


def test_PUT_existing_province(db: Session) -> None:
    created = insert_province(db)

    province_data = {'name': 'Changed'}

    response = client.put(f'/api/v1/province/{created.id}', json=province_data)
    province_from_api = response.json()
    assert response.status_code == 200
    assert province_from_api['name'] == 'Changed'
    crud.province.remove(db, id=created.id)
    crud.country.remove(db, id=created.country_id)


def test_PUT_unexisting_province(db: Session) -> None:
    province_data = {'name': 'Changed'}

    response = client.put('/api/v1/province/0', json=province_data)
    province_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in province_from_api


def test_DELETE_existing_province(db: Session) -> None:
    created = insert_province(db)

    response = client.delete(f'/api/v1/province/{created.id}')
    province_from_api = response.json()
    assert response.status_code == 200
    assert created.name == province_from_api['name']
    crud.province.remove(db, id=created.id)
    crud.country.remove(db, id=created.country_id)


def test_DELETE_unexisting_province(db: Session) -> None:
    response = client.delete('/api/v1/province/0')
    province_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in province_from_api
