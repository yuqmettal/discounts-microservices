from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.city_schema import City, CityCreate, CityUpdate


router = APIRouter()


@router.get("/")
async def get_all_cities(db: Session = Depends(get_db)) -> List[City]:
    return crud.city.filter(db)


@router.post("/")
async def post_city(
    *,
    db: Session = Depends(get_db),
    city: CityCreate
) -> Any:
    city_by_name_and_province = crud.city.get_by_province_and_name(
        db, name=city.name, province_id=city.province_id)
    if city_by_name_and_province:
        raise HTTPException(
            status_code=400,
            detail=f"The city with name '{city.name}' and province id = {city.province_id} already exists",
        )
    return crud.city.create(db, object_to_create=city)


@router.get("/{city_id}", response_model=City)
async def get_city_by_id(
    *,
    db: Session = Depends(get_db),
    city_id: int,
) -> Any:
    city = crud.city.get_by_id(db, id=city_id)
    if not city:
        raise HTTPException(
            status_code=404, detail="The city doesn't exists"
        )
    return city


@router.put("/{city_id}", response_model=City)
def update_city(
    *,
    db: Session = Depends(get_db),
    city_id: int,
    city_update: CityUpdate,
) -> Any:
    city = crud.city.get_by_id(db, id=city_id)
    if not city:
        raise HTTPException(
            status_code=404,
            detail="The city doesn't exists",
        )
    city = crud.city.update(db, db_object=city,
                           object_to_update=city_update)
    return city


@router.delete("/{city_id}", response_model=City)
def delete_city(
    *,
    db: Session = Depends(get_db),
    city_id: int,
) -> Any:
    city = crud.city.get_by_id(db=db, id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    city = crud.city.remove(db=db, id=city_id)
    return city
