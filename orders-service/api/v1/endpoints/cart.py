from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.cart_schema import Cart, CartCreate, CartUpdate


router = APIRouter()


@router.get("/")
async def get_all_carts(db: Session = Depends(get_db)) -> List[Cart]:
    return crud.cart.filter(db)


@router.post("/")
async def post_cart(
    *,
    db: Session = Depends(get_db),
    cart: CartCreate
) -> Any:
    return crud.cart.create(db, object_to_create=cart)


@router.get("/{cart_id}", response_model=Cart)
async def get_cart_by_id(
    *,
    db: Session = Depends(get_db),
    cart_id: int,
) -> Any:
    cart = crud.cart.get_by_id(db, id=cart_id)
    if not cart:
        raise HTTPException(
            status_code=404, detail="The cart doesn't exists"
        )
    return cart


@router.put("/{cart_id}", response_model=Cart)
def update_cart(
    *,
    db: Session = Depends(get_db),
    cart_id: int,
    cart_update: CartUpdate,
) -> Any:
    cart = crud.cart.get_by_id(db, id=cart_id)
    if not cart:
        raise HTTPException(
            status_code=404,
            detail="The cart doesn't exists",
        )
    cart = crud.cart.update(db, db_object=cart,
                           object_to_update=cart_update)
    return cart


@router.delete("/{cart_id}", response_model=Cart)
def delete_cart(
    *,
    db: Session = Depends(get_db),
    cart_id: int,
) -> Any:
    cart = crud.cart.get_by_id(db=db, id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart = crud.cart.remove(db=db, id=cart_id)
    return cart
