from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from app.database import crud
from app.database.schema.product_schema import Product, ProductCreate, ProductUpdate
from test.util.utils import random_upper_string
from test.util.product_util import insert_product, delete_product, create_random_product_data


client = TestClient(app)


def test_GET_product(db: Session) -> None:
    product_count = crud.product.count(db)
    response = client.get('/api/v1/product/')
    assert response.status_code == 200
    assert len(response.json()) == product_count
    created = insert_product(db)

    response = client.get('/api/v1/product/')
    assert response.status_code == 200
    assert len(response.json()) == product_count + 1
    
    delete_product(db, created)


def test_POST_new_product(db: Session) -> None:
    product_data = create_random_product_data()
    response = client.post('/api/v1/product/', json=product_data)

    assert response.status_code == 200

    created_product = response.json()
    product_id = created_product.get("id")

    product_from_db = crud.product.get_by_id(db, product_id)

    assert product_from_db
    assert product_from_db.name == product_data['name']
    
    delete_product(db, product_from_db)


def test_POST_existing_product_name(db: Session) -> None:
    created = insert_product(db)

    product_data = {
        'name': created.name,
        'description': random_upper_string(),
        'tax_rate': 10,
        'brand_id': 1
    }
    response = client.post('/api/v1/product/', json=product_data)

    created_product = response.json()
    assert response.status_code == 400
    assert "_id" not in created_product

    delete_product(db, created)


def test_GET_existing_product(db: Session) -> None:
    created = insert_product(db)

    response = client.get(f'/api/v1/product/{created.id}')
    product_from_api = response.json()
    assert response.status_code == 200
    assert product_from_api['name'] == created.name
    
    delete_product(db, created)


def test_GET_unexisting_product(db: Session) -> None:
    response = client.get('/api/v1/product/0')
    created_product = response.json()
    assert response.status_code == 404
    assert "_id" not in created_product


def test_PUT_existing_product(db: Session) -> None:
    created = insert_product(db)

    product_data = {'name': 'Changed'}

    response = client.put(f'/api/v1/product/{created.id}', json=product_data)
    product_from_api = response.json()
    assert response.status_code == 200
    assert product_from_api['name'] == 'Changed'
    
    delete_product(db, created)


def test_PUT_unexisting_product(db: Session) -> None:
    product_data = {'name': 'Changed'}

    response = client.put('/api/v1/product/0', json=product_data)
    product_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in product_from_api


def test_DELETE_existing_product(db: Session) -> None:
    created = insert_product(db)

    response = client.delete(f'/api/v1/product/{created.id}')
    product_from_api = response.json()
    assert response.status_code == 200
    assert created.name == product_from_api['name']
    
    delete_product(db, created)


def test_DELETE_unexisting_product(db: Session) -> None:
    response = client.delete('/api/v1/product/0')
    product_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in product_from_api
