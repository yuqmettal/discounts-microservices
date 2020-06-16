from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database import crud
from database.schema.client_prime_subscription_schema import ClientPrimeSubscription, ClientPrimeSubscriptionCreate, ClientPrimeSubscriptionUpdate
from test.util.utils import random_upper_string
from test.util.client_prime_subscription_util import insert_client_prime_subscription, delete_client_prime_subscription, create_random_client_prime_subscription_data


client = TestClient(app)


def test_GET_client_prime_subscription(db: Session) -> None:
    client_prime_subscription_count = crud.client_prime_subscription.count(db)
    response = client.get('/api/v1/client_prime_subscription/')
    assert response.status_code == 200
    assert len(response.json()) == client_prime_subscription_count
    created = insert_client_prime_subscription(db)

    response = client.get('/api/v1/client_prime_subscription/')
    assert response.status_code == 200
    assert len(response.json()) == client_prime_subscription_count + 1

    delete_client_prime_subscription(db, created)


def test_POST_new_client_prime_subscription(db: Session) -> None:
    from fastapi.encoders import jsonable_encoder
    client_prime_subscription_data = jsonable_encoder(
        create_random_client_prime_subscription_data())
    response = client.post('/api/v1/client_prime_subscription/',
                           json=client_prime_subscription_data)

    assert response.status_code == 200

    created_client_prime_subscription = response.json()
    client_prime_subscription_id = created_client_prime_subscription.get("id")

    client_prime_subscription_from_db = crud.client_prime_subscription.get_by_id(
        db, client_prime_subscription_id)

    assert client_prime_subscription_from_db
    assert client_prime_subscription_from_db.subscription_state == client_prime_subscription_data[
        'subscription_state']

    delete_client_prime_subscription(db, client_prime_subscription_from_db)


def test_GET_existing_client_prime_subscription(db: Session) -> None:
    created = insert_client_prime_subscription(db)

    response = client.get(f'/api/v1/client_prime_subscription/{created.id}')
    client_prime_subscription_from_api = response.json()
    assert response.status_code == 200
    assert client_prime_subscription_from_api['subscription_state'] == created.subscription_state

    delete_client_prime_subscription(db, created)


def test_GET_unexisting_client_prime_subscription(db: Session) -> None:
    response = client.get('/api/v1/client_prime_subscription/0')
    created_client_prime_subscription = response.json()
    assert response.status_code == 404
    assert "_id" not in created_client_prime_subscription


def test_PUT_existing_client_prime_subscription(db: Session) -> None:
    created = insert_client_prime_subscription(db)

    client_prime_subscription_data = {'subscription_state': 'Changed'}

    response = client.put(
        f'/api/v1/client_prime_subscription/{created.id}', json=client_prime_subscription_data)
    client_prime_subscription_from_api = response.json()
    assert response.status_code == 200
    assert client_prime_subscription_from_api['subscription_state'] == 'Changed'

    delete_client_prime_subscription(db, created)


def test_PUT_unexisting_client_prime_subscription(db: Session) -> None:
    client_prime_subscription_data = {'subscription_state': 'Changed'}

    response = client.put('/api/v1/client_prime_subscription/0',
                          json=client_prime_subscription_data)
    client_prime_subscription_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in client_prime_subscription_from_api


def test_DELETE_existing_client_prime_subscription(db: Session) -> None:
    created = insert_client_prime_subscription(db)

    response = client.delete(f'/api/v1/client_prime_subscription/{created.id}')
    client_prime_subscription_from_api = response.json()
    assert response.status_code == 200
    assert created.subscription_state == client_prime_subscription_from_api[
        'subscription_state']

    delete_client_prime_subscription(db, created)


def test_DELETE_unexisting_client_prime_subscription(db: Session) -> None:
    response = client.delete('/api/v1/client_prime_subscription/0')
    client_prime_subscription_from_api = response.json()
    assert response.status_code == 404
    assert "_id" not in client_prime_subscription_from_api
