from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.cart_item_schema import CartItem, CartItemCreate, CartItemUpdate
from test.util.utils import random_upper_string
from test.util.cart_item_util import insert_cart_item, delete_cart_item, create_random_cart_item_data
from client.base import EurekaResponse


client = TestClient(app)


def test_GET_cart_item(db: Session) -> None:
    cart_item_count = crud.cart_item.count(db)
    response = client.get('/api/v1/cart_item/')
    assert response.status_code == 200
    assert len(response.json()) == cart_item_count
    created = insert_cart_item(db)

    response = client.get('/api/v1/cart_item/')
    assert response.status_code == 200
    assert len(response.json()) == cart_item_count + 1
    
    delete_cart_item(db, created)


def test_POST_new_valid_cart_item(db: Session, mocker) -> None:
    item_response = EurekaResponse(
        200, {'retailer_id': 1, 'product_id': 1, 'id': 1, 'pvp': 100.36, 'category_id': 1, 'margin': 42})
    mocker.patch(
        'client.item_client._item_client.call_remote_service',
        return_value=item_response
    )

    cart_item_data = create_random_cart_item_data()
    response = client.post('/api/v1/cart_item/', json=cart_item_data)

    assert response.status_code == 200

    created_cart_item = response.json()
    cart_item_id = created_cart_item.get("id")

    cart_item_from_db = crud.cart_item.get_by_id(db, cart_item_id)

    assert cart_item_from_db
    assert cart_item_from_db.item_id == cart_item_data['item_id']
    
    delete_cart_item(db, cart_item_from_db)


def test_POST_new_cart_item_invalid_item_id(db: Session, mocker) -> None:
    item_response = EurekaResponse(
        400, {'retailer_id': 1, 'product_id': 1, 'id': 1, 'pvp': 100.36, 'category_id': 1, 'margin': 42})
    mocker.patch(
        'client.item_client._item_client.call_remote_service',
        return_value=item_response
    )

    cart_item_data = create_random_cart_item_data()
    response = client.post('/api/v1/cart_item/', json=cart_item_data)

    created_cart_item = response.json()
    assert response.status_code == 400
    assert "_id" not in created_cart_item


def test_GET_existing_cart_item(db: Session) -> None:
    created = insert_cart_item(db)

    response = client.get(f'/api/v1/cart_item/{created.id}')
    cart_item_from_api = response.json()
    assert response.status_code == 200
    assert cart_item_from_api['item_id'] == created.item_id
    
    delete_cart_item(db, created)


def test_GET_unexisting_cart_item(db: Session) -> None:
    response = client.get('/api/v1/cart_item/0')
    created_cart_item = response.json()
    assert response.status_code == 404
    assert "_id" not in created_cart_item


def test_PUT_existing_cart_item(db: Session) -> None:
    created = insert_cart_item(db)

    cart_item_data = {'item_id': 9}

    response = client.put(f'/api/v1/cart_item/{created.id}', json=cart_item_data)
    cart_item_from_api = response.json()
    assert response.status_code == 200
    assert cart_item_from_api['item_id'] == 9
    
    delete_cart_item(db, created)


def test_PUT_unexisting_cart_item(db: Session) -> None:
    cart_item_data = {'name': 'Changed'}

    response = client.put('/api/v1/cart_item/0', json=cart_item_data)
    cart_item_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in cart_item_from_api


def test_DELETE_existing_cart_item(db: Session) -> None:
    created = insert_cart_item(db)

    response = client.delete(f'/api/v1/cart_item/{created.id}')
    cart_item_from_api = response.json()
    assert response.status_code == 200
    assert created.item_id == cart_item_from_api['item_id']
    
    delete_cart_item(db, created)


def test_DELETE_unexisting_cart_item(db: Session) -> None:
    response = client.delete('/api/v1/cart_item/0')
    cart_item_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in cart_item_from_api
