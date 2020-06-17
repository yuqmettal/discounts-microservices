from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.discount_item_schema import DiscountItem, DiscountItemCreate, DiscountItemUpdate


router = APIRouter()


@router.get("/")
async def get_all_discount_itemes(db: Session = Depends(get_db)) -> List[DiscountItem]:
    return crud.discount_item.filter(db)


@router.post("/")
async def post_discount_item(
    *,
    db: Session = Depends(get_db),
    discount_item: DiscountItemCreate
) -> Any:
    return crud.discount_item.create(db, object_to_create=discount_item)


@router.get("/{discount_item_id}", response_model=DiscountItem)
async def get_discount_item_by_id(
    *,
    db: Session = Depends(get_db),
    discount_item_id: int,
) -> Any:
    discount_item = crud.discount_item.get_by_id(db, id=discount_item_id)
    if not discount_item:
        raise HTTPException(
            status_code=404, detail="The discount_item doesn't exists"
        )
    return discount_item


@router.put("/{discount_item_id}", response_model=DiscountItem)
def update_discount_item(
    *,
    db: Session = Depends(get_db),
    discount_item_id: int,
    discount_item_update: DiscountItemUpdate,
) -> Any:
    discount_item = crud.discount_item.get_by_id(db, id=discount_item_id)
    if not discount_item:
        raise HTTPException(
            status_code=404,
            detail="The discount_item doesn't exists",
        )
    discount_item = crud.discount_item.update(db, db_object=discount_item,
                           object_to_update=discount_item_update)
    return discount_item


@router.delete("/{discount_item_id}", response_model=DiscountItem)
def delete_discount_item(
    *,
    db: Session = Depends(get_db),
    discount_item_id: int,
) -> Any:
    discount_item = crud.discount_item.get_by_id(db=db, id=discount_item_id)
    if not discount_item:
        raise HTTPException(status_code=404, detail="DiscountItem not found")
    discount_item = crud.discount_item.remove(db=db, id=discount_item_id)
    return discount_item
