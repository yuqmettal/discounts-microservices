from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.order_item_schema import OrderItem, OrderItemCreate, OrderItemUpdate
from test.util.utils import random_upper_string
from test.util.order_item_util import insert_order_item, delete_order_item, create_random_order_item_data
from client.base import EurekaResponse


client = TestClient(app)


def test_GET_order_item(db: Session) -> None:
    order_item_count = crud.order_item.count(db)
    response = client.get('/api/v1/order_item/')
    assert response.status_code == 200
    assert len(response.json()) == order_item_count
    created = insert_order_item(db)

    response = client.get('/api/v1/order_item/')
    assert response.status_code == 200
    assert len(response.json()) == order_item_count + 1
    
    delete_order_item(db, created)


def test_POST_new_valid_order_item(db: Session, mocker) -> None:
    item_response = EurekaResponse(
        200, {'retailer_id': 1, 'product_id': 1, 'id': 1, 'pvp': 100.36, 'category_id': 1, 'margin': 42})
    mocker.patch(
        'client.item_client._item_client.call_remote_service',
        return_value=item_response
    )

    order_item_data = create_random_order_item_data()
    response = client.post('/api/v1/order_item/', json=order_item_data)

    assert response.status_code == 200

    created_order_item = response.json()
    order_item_id = created_order_item.get("id")

    order_item_from_db = crud.order_item.get_by_id(db, order_item_id)

    assert order_item_from_db
    assert order_item_from_db.item_id == order_item_data['item_id']
    
    delete_order_item(db, order_item_from_db)


def test_POST_new_order_item_invalid_item_id(db: Session, mocker) -> None:
    item_response = EurekaResponse(
        400, {'retailer_id': 1, 'product_id': 1, 'id': 1, 'pvp': 100.36, 'category_id': 1, 'margin': 42})
    mocker.patch(
        'client.item_client._item_client.call_remote_service',
        return_value=item_response
    )

    order_item_data = create_random_order_item_data()
    response = client.post('/api/v1/order_item/', json=order_item_data)

    created_order_item = response.json()
    assert response.status_code == 400
    assert "_id" not in created_order_item


def test_GET_existing_order_item(db: Session) -> None:
    created = insert_order_item(db)

    response = client.get(f'/api/v1/order_item/{created.id}')
    order_item_from_api = response.json()
    assert response.status_code == 200
    assert order_item_from_api['item_id'] == created.item_id
    
    delete_order_item(db, created)


def test_GET_unexisting_order_item(db: Session) -> None:
    response = client.get('/api/v1/order_item/0')
    created_order_item = response.json()
    assert response.status_code == 404
    assert "_id" not in created_order_item


def test_PUT_existing_order_item(db: Session) -> None:
    created = insert_order_item(db)

    order_item_data = {'item_id': 9}

    response = client.put(f'/api/v1/order_item/{created.id}', json=order_item_data)
    order_item_from_api = response.json()
    assert response.status_code == 200
    assert order_item_from_api['item_id'] == 9
    
    delete_order_item(db, created)


def test_PUT_unexisting_order_item(db: Session) -> None:
    order_item_data = {'name': 'Changed'}

    response = client.put('/api/v1/order_item/0', json=order_item_data)
    order_item_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in order_item_from_api


def test_DELETE_existing_order_item(db: Session) -> None:
    created = insert_order_item(db)

    response = client.delete(f'/api/v1/order_item/{created.id}')
    order_item_from_api = response.json()
    assert response.status_code == 200
    assert created.item_id == order_item_from_api['item_id']
    
    delete_order_item(db, created)


def test_DELETE_unexisting_order_item(db: Session) -> None:
    response = client.delete('/api/v1/order_item/0')
    order_item_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in order_item_from_api
