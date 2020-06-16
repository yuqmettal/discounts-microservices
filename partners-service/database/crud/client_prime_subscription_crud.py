from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import ClientPrimeSubscription
from database.schema.client_prime_subscription_schema import ClientPrimeSubscriptionCreate, ClientPrimeSubscriptionUpdate


class ClientPrimeSubscriptionCRUD(CRUDBase[ClientPrimeSubscription, ClientPrimeSubscriptionCreate, ClientPrimeSubscriptionUpdate]):
    pass


client_prime_subscription = ClientPrimeSubscriptionCRUD(
    ClientPrimeSubscription)
