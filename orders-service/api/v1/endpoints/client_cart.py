from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.client_cart_schema import ClientCart, ClientCartCreate, ClientCartUpdate

from client.partner_client import get_client_by_id


router = APIRouter()


@router.get("/")
async def get_all_client_carts(db: Session = Depends(get_db)) -> List[ClientCart]:
    return crud.client_cart.filter(db)


@router.post("/")
async def post_client_cart(
    *,
    db: Session = Depends(get_db),
    client_cart: ClientCartCreate
) -> Any:
    client = get_client_by_id(client_cart.client_id)
    if not client:
        raise HTTPException(
            status_code=400,
            detail=f"The Client with id '{client_cart.client_id}' does not exists",
        )
    return crud.client_cart.create(db, object_to_create=client_cart)


@router.get("/{client_cart_id}", response_model=ClientCart)
async def get_client_cart_by_id(
    *,
    db: Session = Depends(get_db),
    client_cart_id: int,
) -> Any:
    client_cart = crud.client_cart.get_by_id(db, id=client_cart_id)
    if not client_cart:
        raise HTTPException(
            status_code=404, detail="The client_cart doesn't exists"
        )
    return client_cart


@router.put("/{client_cart_id}", response_model=ClientCart)
def update_client_cart(
    *,
    db: Session = Depends(get_db),
    client_cart_id: int,
    client_cart_update: ClientCartUpdate,
) -> Any:
    client_cart = crud.client_cart.get_by_id(db, id=client_cart_id)
    if not client_cart:
        raise HTTPException(
            status_code=404,
            detail="The client_cart doesn't exists",
        )
    client_cart = crud.client_cart.update(db, db_object=client_cart,
                           object_to_update=client_cart_update)
    return client_cart


@router.delete("/{client_cart_id}", response_model=ClientCart)
def delete_client_cart(
    *,
    db: Session = Depends(get_db),
    client_cart_id: int,
) -> Any:
    client_cart = crud.client_cart.get_by_id(db=db, id=client_cart_id)
    if not client_cart:
        raise HTTPException(status_code=404, detail="ClientCart not found")
    client_cart = crud.client_cart.remove(db=db, id=client_cart_id)
    return client_cart
