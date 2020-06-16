from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.cart_item_schema import CartItem, CartItemCreate, CartItemUpdate

from client.item_client import get_item_by_id


router = APIRouter()


@router.get("/")
async def get_all_cart_items(db: Session = Depends(get_db)) -> List[CartItem]:
    return crud.cart_item.filter(db)


@router.post("/")
async def post_cart_item(
    *,
    db: Session = Depends(get_db),
    cart_item: CartItemCreate
) -> Any:
    item = get_item_by_id(cart_item.item_id)
    if not item:
        raise HTTPException(
            status_code=400,
            detail=f"The Item with id '{cart_item.item_id}' does not exists",
        )
    return crud.cart_item.create(db, object_to_create=cart_item)


@router.get("/{cart_item_id}", response_model=CartItem)
async def get_cart_item_by_id(
    *,
    db: Session = Depends(get_db),
    cart_item_id: int,
) -> Any:
    cart_item = crud.cart_item.get_by_id(db, id=cart_item_id)
    if not cart_item:
        raise HTTPException(
            status_code=404, detail="The cart_item doesn't exists"
        )
    return cart_item


@router.put("/{cart_item_id}", response_model=CartItem)
def update_cart_item(
    *,
    db: Session = Depends(get_db),
    cart_item_id: int,
    cart_item_update: CartItemUpdate,
) -> Any:
    cart_item = crud.cart_item.get_by_id(db, id=cart_item_id)
    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="The cart_item doesn't exists",
        )
    cart_item = crud.cart_item.update(db, db_object=cart_item,
                           object_to_update=cart_item_update)
    return cart_item


@router.delete("/{cart_item_id}", response_model=CartItem)
def delete_cart_item(
    *,
    db: Session = Depends(get_db),
    cart_item_id: int,
) -> Any:
    cart_item = crud.cart_item.get_by_id(db=db, id=cart_item_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="CartItem not found")
    cart_item = crud.cart_item.remove(db=db, id=cart_item_id)
    return cart_item
