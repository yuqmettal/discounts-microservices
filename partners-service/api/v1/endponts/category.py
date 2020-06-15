from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.category_schema import Category, CategoryCreate, CategoryUpdate


router = APIRouter()


@router.get("/")
async def get_all_categoryes(db: Session = Depends(get_db)) -> List[Category]:
    return crud.category.filter(db)


@router.post("/")
async def post_category(
    *,
    db: Session = Depends(get_db),
    category: CategoryCreate
) -> Any:
    category_by_name = crud.category.get_by_name(db, name=category.name)
    if category_by_name:
        raise HTTPException(
            status_code=400,
            detail=f"The Category with name '{category.name}' already exists",
        )
    return crud.category.create(db, object_to_create=category)


@router.get("/{category_id}", response_model=Category)
async def get_category_by_id(
    *,
    db: Session = Depends(get_db),
    category_id: int,
) -> Any:
    category = crud.category.get_by_id(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=404, detail="The category doesn't exists"
        )
    return category


@router.put("/{category_id}", response_model=Category)
def update_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    category_update: CategoryUpdate,
) -> Any:
    category = crud.category.get_by_id(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail="The category doesn't exists",
        )
    category = crud.category.update(db, db_object=category,
                           object_to_update=category_update)
    return category


@router.delete("/{category_id}", response_model=Category)
def delete_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
) -> Any:
    category = crud.category.get_by_id(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.category.remove(db=db, id=category_id)
    return category
