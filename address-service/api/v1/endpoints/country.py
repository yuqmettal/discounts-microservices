from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.crud import country as crud
from api import get_db
from database.schema import Country, CountryCreate, CountryUpdate


router = APIRouter()


@router.get("/")
async def get_all_countries(db: Session = Depends(get_db)) -> List[Country]:
    users = crud.filter(db)
    return users


@router.post("/")
async def post_country(
    *,
    db: Session = Depends(get_db),
    country: CountryCreate
) -> Any:
    country_by_name = crud.get_by_name(db, name=country.name)
    if country_by_name:
        raise HTTPException(
            status_code=400,
            detail=f"The country with name '{country.name}' already exists",
        )
    country_by_code = crud.get_by_code(db, code=country.code)
    if country_by_code:
        raise HTTPException(
            status_code=400,
            detail=f"The country with code '{country.code}' already exists",
        )
    created = crud.create(db, object_to_create=country)
    return created


@router.get("/{country_id}", response_model=Country)
async def get_country_by_id(
    *,
    db: Session = Depends(get_db),
    country_id: int,
) -> Any:
    country = crud.get_by_id(db, id=country_id)
    if not country:
        raise HTTPException(
            status_code=404, detail="The country doesn't exists"
        )
    return country


@router.put("/{country_id}", response_model=Country)
def update_user(
    *,
    db: Session = Depends(get_db),
    country_id: int,
    country_update: CountryUpdate,
) -> Any:
    country = crud.get_by_id(db, id=country_id)
    if not country:
        raise HTTPException(
            status_code=404,
            detail="The country doesn't exists",
        )
    country = crud.update(db, db_object=country, object_to_update=country_update)
    return country


@router.delete("/{country_id}", response_model=Country)
def delete_item(
    *,
    db: Session = Depends(get_db),
    country_id: int,
) -> Any:
    country = crud.get_by_id(db=db, id=country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    country = crud.remove(db=db, id=country_id)
    return country
