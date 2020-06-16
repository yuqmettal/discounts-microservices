from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.item_schema import Item, ItemCreate, ItemUpdate
from client.partner_client import get_category_by_id, get_retailer_by_id


router = APIRouter()


@router.get("/")
async def get_all_items(db: Session = Depends(get_db)) -> List[Item]:
    return crud.item.filter(db)


@router.post("/")
async def post_item(
    *,
    db: Session = Depends(get_db),
    item: ItemCreate
) -> Any:
    category = get_category_by_id(item.category_id)
    if not category:
        raise HTTPException(
            status_code=400,
            detail=f"The Category with id '{item.category_id}' does not exists",
        )
    retailer = get_retailer_by_id(item.retailer_id)
    if not retailer:
        raise HTTPException(
            status_code=400,
            detail=f"The Retailer with id '{item.retailer_id}' does not exists",
        )
    return crud.item.create(db, object_to_create=item)


@router.get("/{item_id}", response_model=Item)
async def get_item_by_id(
    *,
    db: Session = Depends(get_db),
    item_id: int,
) -> Any:
    item = crud.item.get_by_id(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=404, detail="The item doesn't exists"
        )
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    item_update: ItemUpdate,
) -> Any:
    item = crud.item.get_by_id(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail="The item doesn't exists",
        )
    item = crud.item.update(db, db_object=item,
                           object_to_update=item_update)
    return item


@router.delete("/{item_id}", response_model=Item)
def delete_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
) -> Any:
    item = crud.item.get_by_id(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.item.remove(db=db, id=item_id)
    return item
