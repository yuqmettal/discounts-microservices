from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.subcategory_schema import Subcategory, SubcategoryCreate, SubcategoryUpdate


router = APIRouter()


@router.get("/")
async def get_all_subcategories(db: Session = Depends(get_db)) -> List[Subcategory]:
    return crud.subcategory.filter(db)


@router.post("/")
async def post_subcategory(
    *,
    db: Session = Depends(get_db),
    subcategory: SubcategoryCreate
) -> Any:
    subcategory_by_name = crud.subcategory.get_by_name_and_category_id(
        db,
        name=subcategory.name,
        category_id=subcategory.category_id
    )
    if subcategory_by_name:
        raise HTTPException(
            status_code=400,
            detail=f"The Subcategory with name '{subcategory.name}' and category id {subcategory.category_id} already exists",
        )
    return crud.subcategory.create(db, object_to_create=subcategory)


@router.get("/{subcategory_id}", response_model=Subcategory)
async def get_subcategory_by_id(
    *,
    db: Session = Depends(get_db),
    subcategory_id: int,
) -> Any:
    subcategory = crud.subcategory.get_by_id(db, id=subcategory_id)
    if not subcategory:
        raise HTTPException(
            status_code=404, detail="The subcategory doesn't exists"
        )
    return subcategory


@router.put("/{subcategory_id}", response_model=Subcategory)
def update_subcategory(
    *,
    db: Session = Depends(get_db),
    subcategory_id: int,
    subcategory_update: SubcategoryUpdate,
) -> Any:
    subcategory = crud.subcategory.get_by_id(db, id=subcategory_id)
    if not subcategory:
        raise HTTPException(
            status_code=404,
            detail="The subcategory doesn't exists",
        )
    subcategory = crud.subcategory.update(db, db_object=subcategory,
                                          object_to_update=subcategory_update)
    return subcategory


@router.delete("/{subcategory_id}", response_model=Subcategory)
def delete_subcategory(
    *,
    db: Session = Depends(get_db),
    subcategory_id: int,
) -> Any:
    subcategory = crud.subcategory.get_by_id(db=db, id=subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    subcategory = crud.subcategory.remove(db=db, id=subcategory_id)
    return subcategory
