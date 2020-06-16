from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.prime_subscription_schema import PrimeSubscription, PrimeSubscriptionCreate, PrimeSubscriptionUpdate
from test.util.utils import random_upper_string
from test.util.prime_subscription_util import insert_prime_subscription, delete_prime_subscription, create_random_prime_subscription_data


client = TestClient(app)


def test_GET_prime_subscription(db: Session) -> None:
    prime_subscription_count = crud.prime_subscription.count(db)
    response = client.get('/api/v1/prime_subscription/')
    assert response.status_code == 200
    assert len(response.json()) == prime_subscription_count
    created = insert_prime_subscription(db)

    response = client.get('/api/v1/prime_subscription/')
    assert response.status_code == 200
    assert len(response.json()) == prime_subscription_count + 1

    delete_prime_subscription(db, created)


def test_POST_new_prime_subscription(db: Session) -> None:
    prime_subscription_data = create_random_prime_subscription_data()
    response = client.post('/api/v1/prime_subscription/',
                           json=prime_subscription_data)

    assert response.status_code == 200

    created_prime_subscription = response.json()
    prime_subscription_id = created_prime_subscription.get("id")

    prime_subscription_from_db = crud.prime_subscription.get_by_id(
        db, prime_subscription_id)

    assert prime_subscription_from_db
    assert prime_subscription_from_db.name == prime_subscription_data['name']

    delete_prime_subscription(db, prime_subscription_from_db)


def test_POST_existing_prime_subscription_name(db: Session) -> None:
    created = insert_prime_subscription(db)

    prime_subscription_data = {
        'name': created.name,
        'validity': 1,
        'validity_type': random_upper_string(),
        'enabled': True
    }
    response = client.post('/api/v1/prime_subscription/',
                           json=prime_subscription_data)

    created_prime_subscription = response.json()
    assert response.status_code == 400
    assert "_id" not in created_prime_subscription

    delete_prime_subscription(db, created)


def test_GET_existing_prime_subscription(db: Session) -> None:
    created = insert_prime_subscription(db)

    response = client.get(f'/api/v1/prime_subscription/{created.id}')
    prime_subscription_from_api = response.json()
    assert response.status_code == 200
    assert prime_subscription_from_api['name'] == created.name

    delete_prime_subscription(db, created)


def test_GET_unexisting_prime_subscription(db: Session) -> None:
    response = client.get('/api/v1/prime_subscription/0')
    created_prime_subscription = response.json()
    assert response.status_code == 404
    assert "_id" not in created_prime_subscription


def test_PUT_existing_prime_subscription(db: Session) -> None:
    created = insert_prime_subscription(db)

    prime_subscription_data = {'name': 'Changed'}

    response = client.put(
        f'/api/v1/prime_subscription/{created.id}', json=prime_subscription_data)
    prime_subscription_from_api = response.json()
    assert response.status_code == 200
    assert prime_subscription_from_api['name'] == 'Changed'

    delete_prime_subscription(db, created)


def test_PUT_unexisting_prime_subscription(db: Session) -> None:
    prime_subscription_data = {'name': 'Changed'}

    response = client.put('/api/v1/prime_subscription/0',
                          json=prime_subscription_data)
    prime_subscription_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in prime_subscription_from_api


def test_DELETE_existing_prime_subscription(db: Session) -> None:
    created = insert_prime_subscription(db)

    response = client.delete(f'/api/v1/prime_subscription/{created.id}')
    prime_subscription_from_api = response.json()
    assert response.status_code == 200
    assert created.name == prime_subscription_from_api['name']

    delete_prime_subscription(db, created)


def test_DELETE_unexisting_prime_subscription(db: Session) -> None:
    response = client.delete('/api/v1/prime_subscription/0')
    prime_subscription_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in prime_subscription_from_api
