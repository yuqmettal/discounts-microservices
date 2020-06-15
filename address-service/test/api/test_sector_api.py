from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.sector_schema import Sector, SectorCreate, SectorUpdate
from test.util.utils import random_upper_string
from test.util.sector_util import insert_sector, delete_sector, insert_city, create_random_sector_data


client = TestClient(app)


def test_GET_sectors(db: Session) -> None:
    sector_count = crud.sector.count(db)
    response = client.get('/api/v1/sector/')
    assert response.status_code == 200
    assert len(response.json()) == sector_count
    created = insert_sector(db)

    response = client.get('/api/v1/sector/')
    assert response.status_code == 200
    assert len(response.json()) == sector_count + 1
    
    delete_sector(db, created)


def test_POST_new_sector(db: Session) -> None:
    created_sector = insert_city(db)
    sector_data = create_random_sector_data(created_sector.id)
    response = client.post('/api/v1/sector/', json=sector_data)

    assert response.status_code == 200

    created_sector = response.json()
    sector_id = created_sector.get("id")

    sector_from_db = crud.sector.get_by_id(db, sector_id)

    assert sector_from_db
    assert sector_from_db.name == sector_data['name']
    
    delete_sector(db, sector_from_db)


def test_POST_existing_sector_name(db: Session) -> None:
    created = insert_sector(db)

    sector_data = {
        'name': created.name,
        'city_id': created.city_id,
    }
    response = client.post('/api/v1/sector/', json=sector_data)

    created_sector = response.json()
    assert response.status_code == 400
    assert "_id" not in response

    delete_sector(db, created)


def test_GET_existing_sector(db: Session) -> None:
    created = insert_sector(db)

    response = client.get(f'/api/v1/sector/{created.id}')
    sector_from_api = response.json()
    assert response.status_code == 200
    assert sector_from_api['name'] == created.name
    
    delete_sector(db, created)


def test_GET_unexisting_sector(db: Session) -> None:
    response = client.get('/api/v1/sector/0')
    created_sector = response.json()
    assert response.status_code == 404
    assert "_id" not in created_sector


def test_PUT_existing_sector(db: Session) -> None:
    created = insert_sector(db)

    sector_data = {'name': 'Changed'}

    response = client.put(f'/api/v1/sector/{created.id}', json=sector_data)
    sector_from_api = response.json()
    assert response.status_code == 200
    assert sector_from_api['name'] == 'Changed'
    
    delete_sector(db, created)


def test_PUT_unexisting_sector(db: Session) -> None:
    sector_data = {'name': 'Changed'}

    response = client.put('/api/v1/sector/0', json=sector_data)
    sector_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in sector_from_api


def test_DELETE_existing_sector(db: Session) -> None:
    created = insert_sector(db)

    response = client.delete(f'/api/v1/sector/{created.id}')
    sector_from_api = response.json()
    assert response.status_code == 200
    assert created.name == sector_from_api['name']
    
    delete_sector(db, created)


def test_DELETE_unexisting_sector(db: Session) -> None:
    response = client.delete('/api/v1/sector/0')
    sector_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in sector_from_api
