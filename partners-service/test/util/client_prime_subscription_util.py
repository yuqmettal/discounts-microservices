from sqlalchemy.orm import Session
from datetime import date

from database.schema.client_prime_subscription_schema import ClientPrimeSubscriptionCreate, ClientPrimeSubscriptionUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import ClientPrimeSubscription


def create_random_client_prime_subscription() -> ClientPrimeSubscriptionCreate:
    activation_date = date.today()
    subscription_state = random_lower_string()
    client_id = 1
    prime_subscription_id = 1
    return ClientPrimeSubscriptionCreate(activation_date=activation_date, subscription_state=subscription_state, client_id=client_id, prime_subscription_id=prime_subscription_id)


def create_random_client_prime_subscription_data():
    activation_date = date.today()
    subscription_state = random_lower_string()
    client_id = 1
    prime_subscription_id = 1
    return {'activation_date': activation_date, 'subscription_state': subscription_state, 'client_id': client_id, 'prime_subscription_id': prime_subscription_id}


def insert_client_prime_subscription(db: Session):
    client_prime_subscription_create = create_random_client_prime_subscription()
    return crud.client_prime_subscription.create(db, client_prime_subscription_create)


def delete_client_prime_subscription(db: Session, client_prime_subscription: ClientPrimeSubscription):
    crud.client_prime_subscription.remove(db, id=client_prime_subscription.id)
