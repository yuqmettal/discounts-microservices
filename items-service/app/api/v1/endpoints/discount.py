from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import crud
from app.api import get_db
from app.database.schema.discount_schema import Discount, DiscountCreate, DiscountUpdate
from app.client.partner_client import get_category_by_id, get_retailer_by_id


router = APIRouter()


@router.get("/")
async def get_all_discounts(db: Session = Depends(get_db)) -> List[Discount]:
    return crud.discount.filter(db)


@router.post("/")
async def post_discount(
    *,
    db: Session = Depends(get_db),
    discount: DiscountCreate
) -> Any:
    retailer = get_retailer_by_id(discount.retailer_id)
    if not retailer:
        raise HTTPException(
            status_code=400,
            detail=f"The Retailer with id '{discount.retailer_id}' does not exists",
        )
    return crud.discount.create(db, object_to_create=discount)


@router.get("/{discount_id}", response_model=Discount)
async def get_discount_by_id(
    *,
    db: Session = Depends(get_db),
    discount_id: int,
) -> Any:
    discount = crud.discount.get_by_id(db, id=discount_id)
    if not discount:
        raise HTTPException(
            status_code=404, detail="The discount doesn't exists"
        )
    return discount


@router.put("/{discount_id}", response_model=Discount)
def update_discount(
    *,
    db: Session = Depends(get_db),
    discount_id: int,
    discount_update: DiscountUpdate,
) -> Any:
    discount = crud.discount.get_by_id(db, id=discount_id)
    if not discount:
        raise HTTPException(
            status_code=404,
            detail="The discount doesn't exists",
        )
    discount = crud.discount.update(db, db_object=discount,
                           object_to_update=discount_update)
    return discount


@router.delete("/{discount_id}", response_model=Discount)
def delete_discount(
    *,
    db: Session = Depends(get_db),
    discount_id: int,
) -> Any:
    discount = crud.discount.get_by_id(db=db, id=discount_id)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    discount = crud.discount.remove(db=db, id=discount_id)
    return discount
