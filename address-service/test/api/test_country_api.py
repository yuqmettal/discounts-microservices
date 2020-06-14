from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database.crud import country as crud
from database.schema import CountryCreate, CountryUpdate
from test.util.country_util import create_random_country, create_random_country_data
from test.util.utils import random_upper_string


client = TestClient(app)


def test_GET_countries(db: Session) -> None:
    country_count = crud.count(db)
    response = client.get('/api/v1/country/')
    assert response.status_code == 200
    assert len(response.json()) == country_count
    new_country = create_random_country()
    created = crud.create(db, object_to_create=new_country)

    response = client.get('/api/v1/country/')
    assert response.status_code == 200
    assert len(response.json()) == country_count + 1
    crud.remove(db, id=created.id)


def test_POST_new_country(db: Session) -> None:
    country_data = create_random_country_data()
    response = client.post('/api/v1/country/', json=country_data)

    assert response.status_code == 200

    created_country = response.json()
    country_id = created_country.get("id")

    country_from_db = crud.get_by_id(db, country_id)

    assert country_from_db
    assert country_from_db.name == country_data['name']
    crud.remove(db, id=country_id)


def test_POST_existing_country_name(db: Session) -> None:
    country_create = create_random_country()
    created = crud.create(db, country_create)

    country_data = {
        'name': country_create.name,
        'code': random_upper_string(),
        'language': country_create.language,
        'currency': country_create.currency,
    }
    response = client.post('/api/v1/country/', json=country_data)

    created_country = response.json()
    assert response.status_code == 400
    assert "_id" not in response
    crud.remove(db, id=created.id)


def test_POST_existing_country_code(db: Session) -> None:
    country_create = create_random_country()
    created = crud.create(db, country_create)

    country_data = {
        'name': random_upper_string(),
        'code': country_create.code,
        'language': country_create.language,
        'currency': country_create.currency,
    }
    response = client.post('/api/v1/country/', json=country_data)

    created_country = response.json()
    assert response.status_code == 400
    assert "_id" not in created_country
    crud.remove(db, id=created.id)


def test_GET_existing_country(db: Session) -> None:
    country_create = create_random_country()
    created = crud.create(db, country_create)

    response = client.get(f'/api/v1/country/{created.id}')
    country_from_api = response.json()
    assert response.status_code == 200
    assert country_from_api['name'] == country_create.name
    crud.remove(db, id=created.id)


def test_GET_unexisting_country(db: Session) -> None:
    response = client.get('/api/v1/country/0')
    created_country = response.json()
    assert response.status_code == 404
    assert "_id" not in created_country


def test_PUT_existing_country(db: Session) -> None:
    country_create = create_random_country()
    created = crud.create(db, country_create)

    country_data = {'name': 'Changed'}

    response = client.put(f'/api/v1/country/{created.id}', json=country_data)
    country_from_api = response.json()
    assert response.status_code == 200
    assert country_from_api['name'] == 'Changed'
    crud.remove(db, id=created.id)


def test_PUT_unexisting_country(db: Session) -> None:
    country_data = {'name': 'Changed'}

    response = client.put('/api/v1/country/0', json=country_data)
    country_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in country_from_api


def test_DELETE_existing_country(db: Session) -> None:
    country_create = create_random_country()
    created = crud.create(db, country_create)

    response = client.delete(f'/api/v1/country/{created.id}')
    country_from_api = response.json()
    assert response.status_code == 200
    assert country_create.name == country_from_api['name']
    crud.remove(db, id=created.id)


def test_DELETE_unexisting_country(db: Session) -> None:
    response = client.delete('/api/v1/country/0')
    country_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in country_from_api
