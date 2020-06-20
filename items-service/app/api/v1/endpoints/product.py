from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import crud
from app.api import get_db
from app.database.schema.product_schema import Product, ProductCreate, ProductUpdate


router = APIRouter()


@router.get("/")
async def get_all_products(db: Session = Depends(get_db)) -> List[Product]:
    return crud.product.filter(db)


@router.get("/name/{product_name}/")
async def filter_products_by_name(
    *,
    db: Session = Depends(get_db),
    product_name: str,
) -> List[Product]:
    return crud.product.filter_by_name(db, name=product_name)


@router.post("/")
async def post_product(
    *,
    db: Session = Depends(get_db),
    product: ProductCreate
) -> Any:
    product_by_name = crud.product.get_by_name(db, name=product.name)
    if product_by_name:
        raise HTTPException(
            status_code=400,
            detail=f"The Product with name '{product.name}' already exists",
        )
    return crud.product.create(db, object_to_create=product)


@router.get("/{product_id}", response_model=Product)
async def get_product_by_id(
    *,
    db: Session = Depends(get_db),
    product_id: int,
) -> Any:
    product = crud.product.get_by_id(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=404, detail="The product doesn't exists"
        )
    return product


@router.put("/{product_id}", response_model=Product)
def update_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    product_update: ProductUpdate,
) -> Any:
    product = crud.product.get_by_id(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="The product doesn't exists",
        )
    product = crud.product.update(db, db_object=product,
                           object_to_update=product_update)
    return product


@router.delete("/{product_id}", response_model=Product)
def delete_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
) -> Any:
    product = crud.product.get_by_id(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = crud.product.remove(db=db, id=product_id)
    return product
