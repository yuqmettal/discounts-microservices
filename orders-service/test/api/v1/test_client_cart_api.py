from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.client_cart_schema import ClientCart, ClientCartCreate, ClientCartUpdate
from test.util.utils import random_upper_string
from test.util.client_cart_util import insert_client_cart, delete_client_cart, create_random_client_cart_data
from client.base import EurekaResponse


client = TestClient(app)


def test_GET_client_cart(db: Session) -> None:
    client_cart_count = crud.client_cart.count(db)
    response = client.get('/api/v1/client_cart/')
    assert response.status_code == 200
    assert len(response.json()) == client_cart_count
    created = insert_client_cart(db)

    response = client.get('/api/v1/client_cart/')
    assert response.status_code == 200
    assert len(response.json()) == client_cart_count + 1
    
    delete_client_cart(db, created)


def test_POST_new_valid_client_cart(db: Session, mocker) -> None:
    client_response = EurekaResponse(
        200, {'name': "Test", 'last_name': "Mock", 'id': 1, 'email': "mail@mock.com"})
    mocker.patch(
        'client.partner_client._partner_client_client.call_remote_service',
        return_value=client_response
    )

    client_cart_data = create_random_client_cart_data()
    response = client.post('/api/v1/client_cart/', json=client_cart_data)

    assert response.status_code == 200

    created_client_cart = response.json()
    cart_client_id = created_client_cart.get("id")

    client_cart_from_db = crud.client_cart.get_by_id(db, cart_client_id)

    assert client_cart_from_db
    assert client_cart_from_db.client_id == client_cart_data['client_id']
    
    delete_client_cart(db, client_cart_from_db)


def test_POST_new_client_cart_invalid_client_id(db: Session, mocker) -> None:
    client_response = EurekaResponse(
        400, {'name': "Test", 'last_name': "Mock", 'id': 1, 'email': "mail@mock.com"})
    mocker.patch(
        'client.partner_client._partner_client_client.call_remote_service',
        return_value=client_response
    )

    client_cart_data = create_random_client_cart_data()
    response = client.post('/api/v1/client_cart/', json=client_cart_data)

    created_client_cart = response.json()
    assert response.status_code == 400
    assert "_id" not in created_client_cart


def test_GET_existing_client_cart(db: Session) -> None:
    created = insert_client_cart(db)

    response = client.get(f'/api/v1/client_cart/{created.id}')
    client_cart_from_api = response.json()
    assert response.status_code == 200
    assert client_cart_from_api['client_id'] == created.client_id
    
    delete_client_cart(db, created)


def test_GET_unexisting_client_cart(db: Session) -> None:
    response = client.get('/api/v1/client_cart/0')
    created_client_cart = response.json()
    assert response.status_code == 404
    assert "_id" not in created_client_cart


def test_PUT_existing_client_cart(db: Session) -> None:
    created = insert_client_cart(db)

    client_cart_data = {'client_id': 9}

    response = client.put(f'/api/v1/client_cart/{created.id}', json=client_cart_data)
    client_cart_from_api = response.json()
    assert response.status_code == 200
    assert client_cart_from_api['client_id'] == 9
    
    delete_client_cart(db, created)


def test_PUT_unexisting_client_cart(db: Session) -> None:
    client_cart_data = {'name': 'Changed'}

    response = client.put('/api/v1/client_cart/0', json=client_cart_data)
    client_cart_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in client_cart_from_api


def test_DELETE_existing_client_cart(db: Session) -> None:
    created = insert_client_cart(db)

    response = client.delete(f'/api/v1/client_cart/{created.id}')
    client_cart_from_api = response.json()
    assert response.status_code == 200
    assert created.client_id == client_cart_from_api['client_id']
    
    delete_client_cart(db, created)


def test_DELETE_unexisting_client_cart(db: Session) -> None:
    response = client.delete('/api/v1/client_cart/0')
    client_cart_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in client_cart_from_api
