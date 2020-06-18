from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from app.database import crud
from app.database.schema.item_schema import Item, ItemCreate, ItemUpdate
from test.util.utils import random_upper_string
from test.util.item_util import insert_item, delete_item, create_random_item_data
from app.client.base import EurekaResponse


client = TestClient(app)


def test_GET_item(db: Session) -> None:
    item_count = 56
    response = client.get('/api/v1/item/?size=56')
    assert response.status_code == 200
    assert len(response.json()) == item_count
    created = insert_item(db)

    response = client.get(f'/api/v1/item/{created.id}')
    created_item = response.json()
    assert response.status_code == 200
    assert created_item['category_id'] == created.category_id
    
    delete_item(db, created)


def test_POST_new_valid_item(db: Session, mocker) -> None:
    retailer_response = EurekaResponse(
        200, {'name': 'mocked', 'description': 'mocked', 'id': 1, 'city_id': 1, 'category_id': 1, 'category_enabled': True})
    mocker.patch(
        'app.client.partner_client._partner_retailer_client.call_remote_service',
        return_value=retailer_response
    )
    category_response = EurekaResponse(
        200, {'name': 'mocked', 'description': 'mocked', 'id': 1})
    mocker.patch(
        'app.client.partner_client._partner_category_client.call_remote_service',
        return_value=category_response
    )

    item_data = create_random_item_data()
    response = client.post('/api/v1/item/', json=item_data)

    assert response.status_code == 200

    created_item = response.json()
    item_id = created_item.get("id")

    item_from_db = crud.item.get_by_id(db, item_id)

    assert item_from_db
    assert item_from_db.category_id == item_data['category_id']
    
    delete_item(db, item_from_db)


def test_POST_new_item_invalid_retailer_id(db: Session, mocker) -> None:
    retailer_response = EurekaResponse(
        404, {'name': 'mocked', 'description': 'mocked', 'id': 1, 'city_id': 1, 'category_id': 1, 'category_enabled': True})
    mocker.patch(
        'app.client.partner_client._partner_retailer_client.call_remote_service',
        return_value=retailer_response
    )
    category_response = EurekaResponse(
        200, {'name': 'mocked', 'description': 'mocked', 'id': 1})
    mocker.patch(
        'app.client.partner_client._partner_category_client.call_remote_service',
        return_value=category_response
    )

    item_data = create_random_item_data()
    response = client.post('/api/v1/item/', json=item_data)

    created_item = response.json()
    assert response.status_code == 400
    assert "_id" not in created_item


def test_POST_new_item_invalid_category_id(db: Session, mocker) -> None:
    retailer_response = EurekaResponse(
        200, {'name': 'mocked', 'description': 'mocked', 'id': 1, 'city_id': 1, 'category_id': 1, 'category_enabled': True})
    mocker.patch(
        'app.client.partner_client._partner_retailer_client.call_remote_service',
        return_value=retailer_response
    )
    category_response = EurekaResponse(
        400, {'name': 'mocked', 'description': 'mocked', 'id': 1})
    mocker.patch(
        'app.client.partner_client._partner_category_client.call_remote_service',
        return_value=category_response
    )

    item_data = create_random_item_data()
    response = client.post('/api/v1/item/', json=item_data)

    created_item = response.json()
    assert response.status_code == 400
    assert "_id" not in created_item


def test_GET_existing_item(db: Session) -> None:
    created = insert_item(db)

    response = client.get(f'/api/v1/item/{created.id}')
    item_from_api = response.json()
    assert response.status_code == 200
    assert item_from_api['category_id'] == created.category_id
    
    delete_item(db, created)


def test_GET_unexisting_item(db: Session) -> None:
    response = client.get('/api/v1/item/0')
    created_item = response.json()
    assert response.status_code == 404
    assert "_id" not in created_item


def test_PUT_existing_item(db: Session) -> None:
    created = insert_item(db)

    item_data = {'category_id': 9}

    response = client.put(f'/api/v1/item/{created.id}', json=item_data)
    item_from_api = response.json()
    assert response.status_code == 200
    assert item_from_api['category_id'] == 9
    
    delete_item(db, created)


def test_PUT_unexisting_item(db: Session) -> None:
    item_data = {'name': 'Changed'}

    response = client.put('/api/v1/item/0', json=item_data)
    item_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in item_from_api


def test_DELETE_existing_item(db: Session) -> None:
    created = insert_item(db)

    response = client.delete(f'/api/v1/item/{created.id}')
    item_from_api = response.json()
    assert response.status_code == 200
    assert created.product_id == item_from_api['product_id']


def test_DELETE_unexisting_item(db: Session) -> None:
    response = client.delete('/api/v1/item/0')
    item_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in item_from_api
