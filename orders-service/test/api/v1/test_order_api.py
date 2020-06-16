from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.order_schema import Order, OrderCreate, OrderUpdate
from test.util.utils import random_upper_string
from test.util.order_util import insert_order, delete_order, create_random_order_data
from client.base import EurekaResponse


client = TestClient(app)


def test_GET_order(db: Session) -> None:
    order_count = crud.order.count(db)
    response = client.get('/api/v1/order/')
    assert response.status_code == 200
    assert len(response.json()) == order_count
    created = insert_order(db)

    response = client.get('/api/v1/order/')
    assert response.status_code == 200
    assert len(response.json()) == order_count + 1
    
    delete_order(db, created)


def test_POST_new_valid_order(db: Session, mocker) -> None:
    retailer_response = EurekaResponse(
        200, {'name': 'mocked', 'description': 'mocked', 'id': 1, 'city_id': 1, 'category_id': 1, 'category_enabled': True})
    mocker.patch(
        'client.partner_client._partner_retailer_client.call_remote_service',
        return_value=retailer_response
    )
    client_response = EurekaResponse(
        200, {'name': 'mocked', 'last_name': 'mocked', 'id': 1, 'email': 'mail@mock.com'})
    mocker.patch(
        'client.partner_client._partner_client_client.call_remote_service',
        return_value=client_response
    )
    address_response = EurekaResponse(
        200, {'name': 'mocked', 'line_one': 'mocked', 'line_two': 'mocked', 'id': 1, 'sector_id': 1})
    mocker.patch(
        'client.address_client._address_client.call_remote_service',
        return_value=address_response
    )

    order_data = create_random_order_data()
    response = client.post('/api/v1/order/', json=order_data)

    assert response.status_code == 200

    created_order = response.json()
    order_id = created_order.get("id")

    order_from_db = crud.order.get_by_id(db, order_id)

    assert order_from_db
    assert order_from_db.address_id == order_data['address_id']
    
    delete_order(db, order_from_db)


def test_POST_new_order_invalid_retailer_id(db: Session, mocker) -> None:
    retailer_response = EurekaResponse(
        400, {'name': 'mocked', 'description': 'mocked', 'id': 1, 'city_id': 1, 'category_id': 1, 'category_enabled': True})
    mocker.patch(
        'client.partner_client._partner_retailer_client.call_remote_service',
        return_value=retailer_response
    )
    client_response = EurekaResponse(
        200, {'name': 'mocked', 'last_name': 'mocked', 'id': 1, 'email': 'mail@mock.com'})
    mocker.patch(
        'client.partner_client._partner_client_client.call_remote_service',
        return_value=client_response
    )
    address_response = EurekaResponse(
        200, {'name': 'mocked', 'line_one': 'mocked', 'line_two': 'mocked', 'id': 1, 'sector_id': 1})
    mocker.patch(
        'client.address_client._address_client.call_remote_service',
        return_value=address_response
    )

    order_data = create_random_order_data()
    response = client.post('/api/v1/order/', json=order_data)

    created_order = response.json()
    assert response.status_code == 400
    assert "_id" not in created_order


def test_POST_new_order_invalid_client_id(db: Session, mocker) -> None:
    retailer_response = EurekaResponse(
        200, {'name': 'mocked', 'description': 'mocked', 'id': 1, 'city_id': 1, 'category_id': 1, 'category_enabled': True})
    mocker.patch(
        'client.partner_client._partner_retailer_client.call_remote_service',
        return_value=retailer_response
    )
    client_response = EurekaResponse(
        400, {'name': 'mocked', 'last_name': 'mocked', 'id': 1, 'email': 'mail@mock.com'})
    mocker.patch(
        'client.partner_client._partner_client_client.call_remote_service',
        return_value=client_response
    )
    address_response = EurekaResponse(
        200, {'name': 'mocked', 'line_one': 'mocked', 'line_two': 'mocked', 'id': 1, 'sector_id': 1})
    mocker.patch(
        'client.address_client._address_client.call_remote_service',
        return_value=address_response
    )
    order_data = create_random_order_data()
    response = client.post('/api/v1/order/', json=order_data)

    created_order = response.json()
    assert response.status_code == 400
    assert "_id" not in created_order


def test_POST_new_order_invalid_address_id(db: Session, mocker) -> None:
    retailer_response = EurekaResponse(
        200, {'name': 'mocked', 'description': 'mocked', 'id': 1, 'city_id': 1, 'category_id': 1, 'category_enabled': True})
    mocker.patch(
        'client.partner_client._partner_retailer_client.call_remote_service',
        return_value=retailer_response
    )
    client_response = EurekaResponse(
        200, {'name': 'mocked', 'last_name': 'mocked', 'id': 1, 'email': 'mail@mock.com'})
    mocker.patch(
        'client.partner_client._partner_client_client.call_remote_service',
        return_value=client_response
    )
    address_response = EurekaResponse(
        500, {'name': 'mocked', 'line_one': 'mocked', 'line_two': 'mocked', 'id': 1, 'sector_id': 1})
    mocker.patch(
        'client.address_client._address_client.call_remote_service',
        return_value=address_response
    )
    order_data = create_random_order_data()
    response = client.post('/api/v1/order/', json=order_data)

    created_order = response.json()
    assert response.status_code == 400
    assert "_id" not in created_order


def test_GET_existing_order(db: Session) -> None:
    created = insert_order(db)

    response = client.get(f'/api/v1/order/{created.id}')
    order_from_api = response.json()
    assert response.status_code == 200
    assert order_from_api['address_id'] == created.address_id
    
    delete_order(db, created)


def test_GET_unexisting_order(db: Session) -> None:
    response = client.get('/api/v1/order/0')
    created_order = response.json()
    assert response.status_code == 404
    assert "_id" not in created_order


def test_PUT_existing_order(db: Session) -> None:
    created = insert_order(db)

    order_data = {'address_id': 9}

    response = client.put(f'/api/v1/order/{created.id}', json=order_data)
    order_from_api = response.json()
    assert response.status_code == 200
    assert order_from_api['address_id'] == 9
    
    delete_order(db, created)


def test_PUT_unexisting_order(db: Session) -> None:
    order_data = {'name': 'Changed'}

    response = client.put('/api/v1/order/0', json=order_data)
    order_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in order_from_api


def test_DELETE_existing_order(db: Session) -> None:
    created = insert_order(db)

    response = client.delete(f'/api/v1/order/{created.id}')
    order_from_api = response.json()
    assert response.status_code == 200
    assert created.address_id == order_from_api['address_id']
    
    delete_order(db, created)


def test_DELETE_unexisting_order(db: Session) -> None:
    response = client.delete('/api/v1/order/0')
    order_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in order_from_api
