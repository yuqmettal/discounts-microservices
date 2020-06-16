from sqlalchemy.orm import Session

from database.schema.prime_subscription_schema import PrimeSubscriptionCreate, PrimeSubscriptionUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import PrimeSubscription


def create_random_prime_subscription() -> PrimeSubscriptionCreate:
    name = random_lower_string()
    validity = 1
    validity_type = random_lower_string()
    enabled = True
    return PrimeSubscriptionCreate(name=name, validity=validity, validity_type=validity_type, enabled=enabled)


def create_random_prime_subscription_data():
    name = random_lower_string()
    validity = 1
    validity_type = random_lower_string()
    enabled = True
    return {'name': name, 'validity': validity, 'validity_type': validity_type, 'enabled': enabled}


def insert_prime_subscription(db: Session):
    prime_subscription_create = create_random_prime_subscription()
    return crud.prime_subscription.create(db, prime_subscription_create)


def delete_prime_subscription(db: Session, prime_subscription: PrimeSubscription):
    crud.prime_subscription.remove(db, id=prime_subscription.id)
