from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.order_item_schema import OrderItem, OrderItemCreate, OrderItemUpdate

from client.item_client import get_item_by_id


router = APIRouter()


@router.get("/")
async def get_all_order_items(db: Session = Depends(get_db)) -> List[OrderItem]:
    return crud.order_item.filter(db)


@router.post("/")
async def post_order_item(
    *,
    db: Session = Depends(get_db),
    order_item: OrderItemCreate
) -> Any:
    item = get_item_by_id(order_item.item_id)
    if not item:
        raise HTTPException(
            status_code=400,
            detail=f"The Item with id '{order_item.item_id}' does not exists",
        )
    return crud.order_item.create(db, object_to_create=order_item)


@router.get("/{order_item_id}", response_model=OrderItem)
async def get_order_item_by_id(
    *,
    db: Session = Depends(get_db),
    order_item_id: int,
) -> Any:
    order_item = crud.order_item.get_by_id(db, id=order_item_id)
    if not order_item:
        raise HTTPException(
            status_code=404, detail="The order_item doesn't exists"
        )
    return order_item


@router.put("/{order_item_id}", response_model=OrderItem)
def update_order_item(
    *,
    db: Session = Depends(get_db),
    order_item_id: int,
    order_item_update: OrderItemUpdate,
) -> Any:
    order_item = crud.order_item.get_by_id(db, id=order_item_id)
    if not order_item:
        raise HTTPException(
            status_code=404,
            detail="The order_item doesn't exists",
        )
    order_item = crud.order_item.update(db, db_object=order_item,
                           object_to_update=order_item_update)
    return order_item


@router.delete("/{order_item_id}", response_model=OrderItem)
def delete_order_item(
    *,
    db: Session = Depends(get_db),
    order_item_id: int,
) -> Any:
    order_item = crud.order_item.get_by_id(db=db, id=order_item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    order_item = crud.order_item.remove(db=db, id=order_item_id)
    return order_item
