from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.sector_schema import Sector, SectorCreate, SectorUpdate


router = APIRouter()


@router.get("/")
async def get_all_sectors(db: Session = Depends(get_db)) -> List[Sector]:
    return crud.sector.filter(db)


@router.post("/")
async def post_sector(
    *,
    db: Session = Depends(get_db),
    sector: SectorCreate
) -> Any:
    sector_by_name_and_city = crud.sector.get_by_city_and_name(
        db, name=sector.name, city_id=sector.city_id)
    if sector_by_name_and_city:
        raise HTTPException(
            status_code=400,
            detail=f"The sector with name '{sector.name}' and city id = {sector.city_id} already exists",
        )
    return crud.sector.create(db, object_to_create=sector)


@router.get("/{sector_id}", response_model=Sector)
async def get_sector_by_id(
    *,
    db: Session = Depends(get_db),
    sector_id: int,
) -> Any:
    sector = crud.sector.get_by_id(db, id=sector_id)
    if not sector:
        raise HTTPException(
            status_code=404, detail="The sector doesn't exists"
        )
    return sector


@router.put("/{sector_id}", response_model=Sector)
def update_sector(
    *,
    db: Session = Depends(get_db),
    sector_id: int,
    sector_update: SectorUpdate,
) -> Any:
    sector = crud.sector.get_by_id(db, id=sector_id)
    if not sector:
        raise HTTPException(
            status_code=404,
            detail="The sector doesn't exists",
        )
    sector = crud.sector.update(db, db_object=sector,
                           object_to_update=sector_update)
    return sector


@router.delete("/{sector_id}", response_model=Sector)
def delete_sector(
    *,
    db: Session = Depends(get_db),
    sector_id: int,
) -> Any:
    sector = crud.sector.get_by_id(db=db, id=sector_id)
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")
    sector = crud.sector.remove(db=db, id=sector_id)
    return sector
