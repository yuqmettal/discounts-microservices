from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.client_schema import Client, ClientCreate, ClientUpdate
from test.util.utils import random_upper_string
from test.util.client_util import insert_client, delete_client, create_random_client_data


client = TestClient(app)


def test_GET_client(db: Session) -> None:
    client_count = crud.client.count(db)
    response = client.get('/api/v1/client/')
    assert response.status_code == 200
    assert len(response.json()) == client_count
    created = insert_client(db)

    response = client.get('/api/v1/client/')
    assert response.status_code == 200
    assert len(response.json()) == client_count + 1
    
    delete_client(db, created)


def test_POST_new_client(db: Session) -> None:
    client_data = create_random_client_data()
    response = client.post('/api/v1/client/', json=client_data)

    assert response.status_code == 200

    created_client = response.json()
    client_id = created_client.get("id")

    client_from_db = crud.client.get_by_id(db, client_id)

    assert client_from_db
    assert client_from_db.name == client_data['name']
    
    delete_client(db, client_from_db)


def test_POST_existing_client_email(db: Session) -> None:
    created = insert_client(db)

    client_data = {
        'name': random_upper_string(),
        'email': created.email,
        'last_name': random_upper_string(),
    }
    response = client.post('/api/v1/client/', json=client_data)

    created_client = response.json()
    assert response.status_code == 400
    assert "_id" not in created_client

    delete_client(db, created)


def test_GET_existing_client(db: Session) -> None:
    created = insert_client(db)

    response = client.get(f'/api/v1/client/{created.id}')
    client_from_api = response.json()
    assert response.status_code == 200
    assert client_from_api['name'] == created.name
    
    delete_client(db, created)


def test_GET_unexisting_client(db: Session) -> None:
    response = client.get('/api/v1/client/0')
    created_client = response.json()
    assert response.status_code == 404
    assert "_id" not in created_client


def test_PUT_existing_client(db: Session) -> None:
    created = insert_client(db)

    client_data = {'name': 'Changed'}

    response = client.put(f'/api/v1/client/{created.id}', json=client_data)
    client_from_api = response.json()
    assert response.status_code == 200
    assert client_from_api['name'] == 'Changed'
    
    delete_client(db, created)


def test_PUT_unexisting_client(db: Session) -> None:
    client_data = {'name': 'Changed'}

    response = client.put('/api/v1/client/0', json=client_data)
    client_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in client_from_api


def test_DELETE_existing_client(db: Session) -> None:
    created = insert_client(db)

    response = client.delete(f'/api/v1/client/{created.id}')
    client_from_api = response.json()
    assert response.status_code == 200
    assert created.name == client_from_api['name']
    
    delete_client(db, created)


def test_DELETE_unexisting_client(db: Session) -> None:
    response = client.delete('/api/v1/client/0')
    client_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in client_from_api