from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import crud
from app.api import get_db
from app.database.schema.brand_schema import Brand, BrandCreate, BrandUpdate


router = APIRouter()


@router.get("/")
async def get_all_brandes(db: Session = Depends(get_db)) -> List[Brand]:
    return crud.brand.filter(db)


@router.post("/")
async def post_brand(
    *,
    db: Session = Depends(get_db),
    brand: BrandCreate
) -> Any:
    brand_by_name = crud.brand.get_by_name(db, name=brand.name)
    if brand_by_name:
        raise HTTPException(
            status_code=400,
            detail=f"The Brand with name '{brand.name}' already exists",
        )
    return crud.brand.create(db, object_to_create=brand)


@router.get("/{brand_id}", response_model=Brand)
async def get_brand_by_id(
    *,
    db: Session = Depends(get_db),
    brand_id: int,
) -> Any:
    brand = crud.brand.get_by_id(db, id=brand_id)
    if not brand:
        raise HTTPException(
            status_code=404, detail="The brand doesn't exists"
        )
    return brand


@router.put("/{brand_id}", response_model=Brand)
def update_brand(
    *,
    db: Session = Depends(get_db),
    brand_id: int,
    brand_update: BrandUpdate,
) -> Any:
    brand = crud.brand.get_by_id(db, id=brand_id)
    if not brand:
        raise HTTPException(
            status_code=404,
            detail="The brand doesn't exists",
        )
    brand = crud.brand.update(db, db_object=brand,
                           object_to_update=brand_update)
    return brand


@router.delete("/{brand_id}", response_model=Brand)
def delete_brand(
    *,
    db: Session = Depends(get_db),
    brand_id: int,
) -> Any:
    brand = crud.brand.get_by_id(db=db, id=brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    brand = crud.brand.remove(db=db, id=brand_id)
    return brand
