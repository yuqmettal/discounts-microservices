from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.client_prime_subscription_schema import ClientPrimeSubscription, ClientPrimeSubscriptionCreate, ClientPrimeSubscriptionUpdate


router = APIRouter()


@router.get("/")
async def get_all_client_prime_subscriptions(db: Session = Depends(get_db)) -> List[ClientPrimeSubscription]:
    return crud.client_prime_subscription.filter(db)


@router.post("/")
async def post_client_prime_subscription(
    *,
    db: Session = Depends(get_db),
    client_prime_subscription: ClientPrimeSubscriptionCreate
) -> Any:
    return crud.client_prime_subscription.create(db, object_to_create=client_prime_subscription)


@router.get("/{client_prime_subscription_id}", response_model=ClientPrimeSubscription)
async def get_client_prime_subscription_by_id(
    *,
    db: Session = Depends(get_db),
    client_prime_subscription_id: int,
) -> Any:
    client_prime_subscription = crud.client_prime_subscription.get_by_id(db, id=client_prime_subscription_id)
    if not client_prime_subscription:
        raise HTTPException(
            status_code=404, detail="The client_prime_subscription doesn't exists"
        )
    return client_prime_subscription


@router.put("/{client_prime_subscription_id}", response_model=ClientPrimeSubscription)
def update_client_prime_subscription(
    *,
    db: Session = Depends(get_db),
    client_prime_subscription_id: int,
    client_prime_subscription_update: ClientPrimeSubscriptionUpdate,
) -> Any:
    client_prime_subscription = crud.client_prime_subscription.get_by_id(db, id=client_prime_subscription_id)
    if not client_prime_subscription:
        raise HTTPException(
            status_code=404,
            detail="The client_prime_subscription doesn't exists",
        )
    client_prime_subscription = crud.client_prime_subscription.update(db, db_object=client_prime_subscription,
                           object_to_update=client_prime_subscription_update)
    return client_prime_subscription


@router.delete("/{client_prime_subscription_id}", response_model=ClientPrimeSubscription)
def delete_client_prime_subscription(
    *,
    db: Session = Depends(get_db),
    client_prime_subscription_id: int,
) -> Any:
    client_prime_subscription = crud.client_prime_subscription.get_by_id(db=db, id=client_prime_subscription_id)
    if not client_prime_subscription:
        raise HTTPException(status_code=404, detail="ClientPrimeSubscription not found")
    client_prime_subscription = crud.client_prime_subscription.remove(db=db, id=client_prime_subscription_id)
    return client_prime_subscription
