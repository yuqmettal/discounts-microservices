from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import PrimeSubscription
from database.schema.prime_subscription_schema import PrimeSubscriptionCreate, PrimeSubscriptionUpdate


class PrimeSubscriptionCRUD(CRUDBase[PrimeSubscription, PrimeSubscriptionCreate, PrimeSubscriptionUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(PrimeSubscription).filter(PrimeSubscription.name == name).first()


prime_subscription = PrimeSubscriptionCRUD(PrimeSubscription)
