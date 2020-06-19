from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.retailer_schema import Retailer, RetailerCreate, RetailerUpdate
from client.address_client import get_city_by_id


router = APIRouter()


@router.get("/")
async def get_all_retailers(db: Session = Depends(get_db)) -> List[Retailer]:
    return crud.retailer.filter(db)


@router.post("/category/")
async def get_all_retailers_by_category(
    *,
    db: Session = Depends(get_db),
    categories: List[int],
) -> Any:
    return crud.retailer_category.get_by_categories(db, categories=categories)


@router.post("/subcategory/")
async def get_all_retailers_by_subcategory(
    *,
    db: Session = Depends(get_db),
    subcategories: List[int],
) -> Any:
    categories = crud.subcategory.get_category_ids_from_subcategories(db, subcategories=subcategories)
    return crud.retailer_category.get_by_categories(db, categories= categories)


@router.post("/")
async def post_retailer(
    *,
    db: Session = Depends(get_db),
    retailer: RetailerCreate
) -> Any:
    retailer_by_name = crud.retailer.get_by_name(
        db,
        name=retailer.name
    )
    if retailer_by_name:
        raise HTTPException(
            status_code=400,
            detail=f"The Retailer with name '{retailer.name}' already exists",
        )
    city = get_city_by_id(retailer.city_id)
    if not city:
        raise HTTPException(
            status_code=400,
            detail=f"The City with id '{retailer.city_id}' does not exists",
        )

    return crud.retailer.create(db, object_to_create=retailer)


@router.get("/{retailer_id}", response_model=Retailer)
async def get_retailer_by_id(
    *,
    db: Session = Depends(get_db),
    retailer_id: int,
) -> Any:
    retailer = crud.retailer.get_by_id(db, id=retailer_id)
    if not retailer:
        raise HTTPException(
            status_code=404, detail="The retailer doesn't exists"
        )
    return retailer


@router.put("/{retailer_id}", response_model=Retailer)
def update_retailer(
    *,
    db: Session = Depends(get_db),
    retailer_id: int,
    retailer_update: RetailerUpdate,
) -> Any:
    retailer = crud.retailer.get_by_id(db, id=retailer_id)
    if not retailer:
        raise HTTPException(
            status_code=404,
            detail="The retailer doesn't exists",
        )
    retailer = crud.retailer.update(db, db_object=retailer,
                                    object_to_update=retailer_update)
    return retailer


@router.delete("/{retailer_id}", response_model=Retailer)
def delete_retailer(
    *,
    db: Session = Depends(get_db),
    retailer_id: int,
) -> Any:
    retailer = crud.retailer.get_by_id(db=db, id=retailer_id)
    if not retailer:
        raise HTTPException(status_code=404, detail="Retailer not found")
    retailer = crud.retailer.remove(db=db, id=retailer_id)
    return retailer
