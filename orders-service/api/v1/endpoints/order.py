from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.order_schema import Order, OrderCreate, OrderUpdate

from client.partner_client import get_retailer_by_id, get_client_by_id
from client.address_client import get_address_by_id


router = APIRouter()


@router.get("/")
async def get_all_orders(db: Session = Depends(get_db)) -> List[Order]:
    return crud.order.filter(db)


@router.post("/")
async def post_order(
    *,
    db: Session = Depends(get_db),
    order: OrderCreate
) -> Any:
    client = get_client_by_id(order.client_id)
    if not client:
        raise HTTPException(
            status_code=400,
            detail=f"The Client with id '{order.client_id}' does not exists",
        )
    retailer = get_retailer_by_id(order.retailer_id)
    if not retailer:
        raise HTTPException(
            status_code=400,
            detail=f"The Retailer with id '{order.retailer_id}' does not exists",
        )
    address = get_address_by_id(order.address_id)
    if not address:
        raise HTTPException(
            status_code=400,
            detail=f"The Address with id '{order.address_id}' does not exists",
        )
    return crud.order.create(db, object_to_create=order)


@router.get("/{order_id}", response_model=Order)
async def get_order_by_id(
    *,
    db: Session = Depends(get_db),
    order_id: int,
) -> Any:
    order = crud.order.get_by_id(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=404, detail="The order doesn't exists"
        )
    return order


@router.put("/{order_id}", response_model=Order)
def update_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    order_update: OrderUpdate,
) -> Any:
    order = crud.order.get_by_id(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="The order doesn't exists",
        )
    order = crud.order.update(db, db_object=order,
                           object_to_update=order_update)
    return order


@router.delete("/{order_id}", response_model=Order)
def delete_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
) -> Any:
    order = crud.order.get_by_id(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order = crud.order.remove(db=db, id=order_id)
    return order
