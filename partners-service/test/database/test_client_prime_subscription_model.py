from sqlalchemy.orm import Session

from database import crud
from database.schema.client_prime_subscription_schema import ClientPrimeSubscriptionCreate, ClientPrimeSubscriptionUpdate
from test.util.client_prime_subscription_util import insert_client_prime_subscription, delete_client_prime_subscription


def test_list_all_client_prime_subscriptions(db: Session) -> None:
    client_prime_subscription_count = crud.client_prime_subscription.count(db)
    client_prime_subscriptions = crud.client_prime_subscription.filter(db)
    assert len(client_prime_subscriptions) == client_prime_subscription_count
    created = insert_client_prime_subscription(db)
    client_prime_subscriptions = crud.client_prime_subscription.filter(db)
    assert len(client_prime_subscriptions) == client_prime_subscription_count + 1
    delete_client_prime_subscription(db, created)


def test_create_client_prime_subscription(db: Session) -> None:
    created = insert_client_prime_subscription(db)
    client_prime_subscription_created = crud.client_prime_subscription.get_by_id(db, created.id)
    assert created.id == client_prime_subscription_created.id
    assert created.subscription_state == client_prime_subscription_created.subscription_state
    delete_client_prime_subscription(db, created)


def test_update_client_prime_subscription(db: Session) -> None:
    created = insert_client_prime_subscription(db)
    client_prime_subscription_from_db = crud.client_prime_subscription.get_by_id(db, created.id)
    client_prime_subscription_update = ClientPrimeSubscriptionUpdate(subscription_state="Changed")
    updated_client_prime_subscription = crud.client_prime_subscription.update(
        db, db_object=client_prime_subscription_from_db, object_to_update=client_prime_subscription_update)
    client_prime_subscription_from_db = crud.client_prime_subscription.get_by_id(db, created.id)
    assert client_prime_subscription_from_db.id == updated_client_prime_subscription.id
    assert client_prime_subscription_from_db.subscription_state == "Changed"
    delete_client_prime_subscription(db, created)


def test_delete_client_prime_subscription(db: Session) -> None:
    created = insert_client_prime_subscription(db)

    client_prime_subscription_from_db = crud.client_prime_subscription.get_by_id(db, created.id)
    assert client_prime_subscription_from_db
    deleted = crud.client_prime_subscription.remove(db, id=created.id)
    client_prime_subscription_from_db = crud.client_prime_subscription.get_by_id(db, created.id)
    assert client_prime_subscription_from_db is None
    assert deleted.id == created.id
