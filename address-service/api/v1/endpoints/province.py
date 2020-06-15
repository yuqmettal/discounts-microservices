from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema import Province, ProvinceCreate, ProvinceUpdate


router = APIRouter()


@router.get("/")
async def get_all_provinces(db: Session = Depends(get_db)) -> List[Province]:
    return crud.province.filter(db)


@router.post("/")
async def post_province(
    *,
    db: Session = Depends(get_db),
    province: ProvinceCreate
) -> Any:
    province_by_name_and_country = crud.province.get_by_country_and_name(
        db, name=province.name, country_id=province.country_id)
    if province_by_name_and_country:
        raise HTTPException(
            status_code=400,
            detail=f"The province with name '{province.name}' and country id = {province.country_id} already exists",
        )
    return crud.province.create(db, object_to_create=province)


@router.get("/{province_id}", response_model=Province)
async def get_province_by_id(
    *,
    db: Session = Depends(get_db),
    province_id: int,
) -> Any:
    province = crud.province.get_by_id(db, id=province_id)
    if not province:
        raise HTTPException(
            status_code=404, detail="The province doesn't exists"
        )
    return province


@router.put("/{province_id}", response_model=Province)
def update_province(
    *,
    db: Session = Depends(get_db),
    province_id: int,
    province_update: ProvinceUpdate,
) -> Any:
    province = crud.province.get_by_id(db, id=province_id)
    if not province:
        raise HTTPException(
            status_code=404,
            detail="The province doesn't exists",
        )
    province = crud.province.update(db, db_object=province,
                           object_to_update=province_update)
    return province


@router.delete("/{province_id}", response_model=Province)
def delete_province(
    *,
    db: Session = Depends(get_db),
    province_id: int,
) -> Any:
    province = crud.province.get_by_id(db=db, id=province_id)
    if not province:
        raise HTTPException(status_code=404, detail="Province not found")
    province = crud.province.remove(db=db, id=province_id)
    return province
