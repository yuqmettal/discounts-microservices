from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.cart_schema import Cart, CartCreate, CartUpdate
from test.util.utils import random_upper_string
from test.util.cart_util import insert_cart, delete_cart, create_random_cart_data


client = TestClient(app)


def test_GET_cart(db: Session) -> None:
    cart_count = crud.cart.count(db)
    response = client.get('/api/v1/cart/')
    assert response.status_code == 200
    assert len(response.json()) == cart_count
    created = insert_cart(db)

    response = client.get('/api/v1/cart/')
    assert response.status_code == 200
    assert len(response.json()) == cart_count + 1
    
    delete_cart(db, created)


def test_POST_new_valid_cart(db: Session, mocker) -> None:
    cart_data = create_random_cart_data()
    response = client.post('/api/v1/cart/', json=cart_data)

    assert response.status_code == 200

    created_cart = response.json()
    cart_id = created_cart.get("id")

    cart_from_db = crud.cart.get_by_id(db, cart_id)

    assert cart_from_db
    assert cart_from_db.name == cart_data['name']
    
    delete_cart(db, cart_from_db)


def test_GET_existing_cart(db: Session) -> None:
    created = insert_cart(db)

    response = client.get(f'/api/v1/cart/{created.id}')
    cart_from_api = response.json()
    assert response.status_code == 200
    assert cart_from_api['name'] == created.name
    
    delete_cart(db, created)


def test_GET_unexisting_cart(db: Session) -> None:
    response = client.get('/api/v1/cart/0')
    created_cart = response.json()
    assert response.status_code == 404
    assert "_id" not in created_cart


def test_PUT_existing_cart(db: Session) -> None:
    created = insert_cart(db)

    cart_data = {'name': "Changed"}

    response = client.put(f'/api/v1/cart/{created.id}', json=cart_data)
    cart_from_api = response.json()
    assert response.status_code == 200
    assert cart_from_api['name'] == "Changed"
    
    delete_cart(db, created)


def test_PUT_unexisting_cart(db: Session) -> None:
    cart_data = {'name': 'Changed'}

    response = client.put('/api/v1/cart/0', json=cart_data)
    cart_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in cart_from_api


def test_DELETE_existing_cart(db: Session) -> None:
    created = insert_cart(db)

    response = client.delete(f'/api/v1/cart/{created.id}')
    cart_from_api = response.json()
    assert response.status_code == 200
    assert created.name == cart_from_api['name']
    
    delete_cart(db, created)


def test_DELETE_unexisting_cart(db: Session) -> None:
    response = client.delete('/api/v1/cart/0')
    cart_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in cart_from_api
