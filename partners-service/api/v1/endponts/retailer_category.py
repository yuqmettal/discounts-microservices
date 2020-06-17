from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.retailer_category_schema import RetailerCategory, RetailerCategoryCreate, RetailerCategoryUpdate


router = APIRouter()


@router.get("/")
async def get_all_retailer_categorys(db: Session = Depends(get_db)) -> List[RetailerCategory]:
    return crud.retailer_category.filter(db)


@router.post("/")
async def post_retailer_category(
    *,
    db: Session = Depends(get_db),
    retailer_category: RetailerCategoryCreate
) -> Any:
    return crud.retailer_category.create(db, object_to_create=retailer_category)


@router.get("/{retailer_category_id}", response_model=RetailerCategory)
async def get_retailer_category_by_id(
    *,
    db: Session = Depends(get_db),
    retailer_category_id: int,
) -> Any:
    retailer_category = crud.retailer_category.get_by_id(db, id=retailer_category_id)
    if not retailer_category:
        raise HTTPException(
            status_code=404, detail="The retailer_category doesn't exists"
        )
    return retailer_category


@router.put("/{retailer_category_id}", response_model=RetailerCategory)
def update_retailer_category(
    *,
    db: Session = Depends(get_db),
    retailer_category_id: int,
    retailer_category_update: RetailerCategoryUpdate,
) -> Any:
    retailer_category = crud.retailer_category.get_by_id(db, id=retailer_category_id)
    if not retailer_category:
        raise HTTPException(
            status_code=404,
            detail="The retailer_category doesn't exists",
        )
    retailer_category = crud.retailer_category.update(db, db_object=retailer_category,
                                          object_to_update=retailer_category_update)
    return retailer_category


@router.delete("/{retailer_category_id}", response_model=RetailerCategory)
def delete_retailer_category(
    *,
    db: Session = Depends(get_db),
    retailer_category_id: int,
) -> Any:
    retailer_category = crud.retailer_category.get_by_id(db=db, id=retailer_category_id)
    if not retailer_category:
        raise HTTPException(status_code=404, detail="RetailerCategory not found")
    retailer_category = crud.retailer_category.remove(db=db, id=retailer_category_id)
    return retailer_category
