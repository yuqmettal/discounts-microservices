from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from app.database import crud
from app.database.schema.discount_schema import Discount, DiscountCreate, DiscountUpdate
from test.util.utils import random_upper_string
from test.util.discount_util import insert_discount, delete_discount, create_random_discount_data
from app.client.base import EurekaResponse


client = TestClient(app)


def test_GET_discount(db: Session) -> None:
    discount_count = crud.discount.count(db)
    response = client.get('/api/v1/discount/')
    assert response.status_code == 200
    assert len(response.json()) == discount_count
    created = insert_discount(db)

    response = client.get('/api/v1/discount/')
    assert response.status_code == 200
    assert len(response.json()) == discount_count + 1
    
    delete_discount(db, created)


def test_POST_new_valid_discount(db: Session, mocker) -> None:
    retailer_response = EurekaResponse(
        200, {'name': 'mocked', 'description': 'mocked', 'id': 1, 'city_id': 1})
    mocker.patch(
        'app.client.partner_client._partner_retailer_client.call_remote_service',
        return_value=retailer_response
    )

    discount_data = create_random_discount_data()
    response = client.post('/api/v1/discount/', json={"discount": discount_data})

    assert response.status_code == 200

    created_discount = response.json()
    discount_id = created_discount.get("id")

    discount_from_db = crud.discount.get_by_id(db, discount_id)

    assert discount_from_db
    assert discount_from_db.retailer_id == discount_data['retailer_id']
    
    delete_discount(db, discount_from_db)


def test_POST_new_discount_invalid_retailer_id(db: Session, mocker) -> None:
    retailer_response = EurekaResponse(
        404, {'name': 'mocked', 'description': 'mocked', 'id': 1, 'city_id': 1, 'category_id': 1, 'category_enabled': True})
    mocker.patch(
        'app.client.partner_client._partner_retailer_client.call_remote_service',
        return_value=retailer_response
    )

    discount_data = create_random_discount_data()
    response = client.post('/api/v1/discount/', json={"discount": discount_data})

    created_discount = response.json()
    assert response.status_code == 400
    assert "_id" not in created_discount


def test_GET_existing_discount(db: Session) -> None:
    created = insert_discount(db)

    response = client.get(f'/api/v1/discount/{created.id}')
    discount_from_api = response.json()
    assert response.status_code == 200
    assert discount_from_api['retailer_id'] == created.retailer_id
    
    delete_discount(db, created)


def test_GET_unexisting_discount(db: Session) -> None:
    response = client.get('/api/v1/discount/0')
    created_discount = response.json()
    assert response.status_code == 404
    assert "_id" not in created_discount


def test_PUT_existing_discount(db: Session) -> None:
    created = insert_discount(db)

    discount_data = {'retailer_id': 9}

    response = client.put(f'/api/v1/discount/{created.id}', json=discount_data)
    discount_from_api = response.json()
    assert response.status_code == 200
    assert discount_from_api['retailer_id'] == 9
    
    delete_discount(db, created)


def test_PUT_unexisting_discount(db: Session) -> None:
    discount_data = {'name': 'Changed'}

    response = client.put('/api/v1/discount/0', json=discount_data)
    discount_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in discount_from_api


def test_DELETE_existing_discount(db: Session) -> None:
    created = insert_discount(db)

    response = client.delete(f'/api/v1/discount/{created.id}')
    discount_from_api = response.json()
    assert response.status_code == 200
    assert created.retailer_id == discount_from_api['retailer_id']
    
    delete_discount(db, created)


def test_DELETE_unexisting_discount(db: Session) -> None:
    response = client.delete('/api/v1/discount/0')
    discount_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in discount_from_api
