from sqlalchemy.orm import Session

from database import crud
from database.schema.prime_subscription_schema import PrimeSubscriptionCreate, PrimeSubscriptionUpdate
from test.util.prime_subscription_util import insert_prime_subscription, delete_prime_subscription


def test_list_all_prime_subscriptions(db: Session) -> None:
    prime_subscription_count = crud.prime_subscription.count(db)
    prime_subscriptions = crud.prime_subscription.filter(db)
    assert len(prime_subscriptions) == prime_subscription_count
    created = insert_prime_subscription(db)
    prime_subscriptions = crud.prime_subscription.filter(db)
    assert len(prime_subscriptions) == prime_subscription_count + 1
    delete_prime_subscription(db, created)


def test_create_prime_subscription(db: Session) -> None:
    created = insert_prime_subscription(db)
    prime_subscription_created = crud.prime_subscription.get_by_id(db, created.id)
    assert created.id == prime_subscription_created.id
    assert created.name == prime_subscription_created.name
    delete_prime_subscription(db, created)


def test_update_prime_subscription(db: Session) -> None:
    created = insert_prime_subscription(db)
    prime_subscription_from_db = crud.prime_subscription.get_by_id(db, created.id)
    prime_subscription_update = PrimeSubscriptionUpdate(name="Changed")
    updated_prime_subscription = crud.prime_subscription.update(
        db, db_object=prime_subscription_from_db, object_to_update=prime_subscription_update)
    prime_subscription_from_db = crud.prime_subscription.get_by_id(db, created.id)
    assert prime_subscription_from_db.id == updated_prime_subscription.id
    assert prime_subscription_from_db.name == "Changed"
    delete_prime_subscription(db, created)


def test_delete_prime_subscription(db: Session) -> None:
    created = insert_prime_subscription(db)

    prime_subscription_from_db = crud.prime_subscription.get_by_id(db, created.id)
    assert prime_subscription_from_db
    deleted = crud.prime_subscription.remove(db, id=created.id)
    prime_subscription_from_db = crud.prime_subscription.get_by_id(db, created.id)
    assert prime_subscription_from_db is None
    assert deleted.id == created.id
