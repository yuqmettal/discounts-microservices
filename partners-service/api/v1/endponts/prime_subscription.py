from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.prime_subscription_schema import PrimeSubscription, PrimeSubscriptionCreate, PrimeSubscriptionUpdate


router = APIRouter()


@router.get("/")
async def get_all_prime_subscriptions(db: Session = Depends(get_db)) -> List[PrimeSubscription]:
    return crud.prime_subscription.filter(db)


@router.post("/")
async def post_prime_subscription(
    *,
    db: Session = Depends(get_db),
    prime_subscription: PrimeSubscriptionCreate
) -> Any:
    prime_subscription_by_name = crud.prime_subscription.get_by_name(db, name=prime_subscription.name)
    if prime_subscription_by_name:
        raise HTTPException(
            status_code=400,
            detail=f"The Prime Subscription with name '{prime_subscription.name}' already exists",
        )
    return crud.prime_subscription.create(db, object_to_create=prime_subscription)


@router.get("/{prime_subscription_id}", response_model=PrimeSubscription)
async def get_prime_subscription_by_id(
    *,
    db: Session = Depends(get_db),
    prime_subscription_id: int,
) -> Any:
    prime_subscription = crud.prime_subscription.get_by_id(db, id=prime_subscription_id)
    if not prime_subscription:
        raise HTTPException(
            status_code=404, detail="The prime_subscription doesn't exists"
        )
    return prime_subscription


@router.put("/{prime_subscription_id}", response_model=PrimeSubscription)
def update_prime_subscription(
    *,
    db: Session = Depends(get_db),
    prime_subscription_id: int,
    prime_subscription_update: PrimeSubscriptionUpdate,
) -> Any:
    prime_subscription = crud.prime_subscription.get_by_id(db, id=prime_subscription_id)
    if not prime_subscription:
        raise HTTPException(
            status_code=404,
            detail="The prime_subscription doesn't exists",
        )
    prime_subscription = crud.prime_subscription.update(db, db_object=prime_subscription,
                           object_to_update=prime_subscription_update)
    return prime_subscription


@router.delete("/{prime_subscription_id}", response_model=PrimeSubscription)
def delete_prime_subscription(
    *,
    db: Session = Depends(get_db),
    prime_subscription_id: int,
) -> Any:
    prime_subscription = crud.prime_subscription.get_by_id(db=db, id=prime_subscription_id)
    if not prime_subscription:
        raise HTTPException(status_code=404, detail="PrimeSubscription not found")
    prime_subscription = crud.prime_subscription.remove(db=db, id=prime_subscription_id)
    return prime_subscription
