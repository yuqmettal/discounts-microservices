from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.retailer_sector_schema import RetailerSector, RetailerSectorCreate, RetailerSectorUpdate
from client.address_client import get_sector_by_id


router = APIRouter()


@router.get("/")
async def get_all_retailer_sectors(db: Session = Depends(get_db)) -> List[RetailerSector]:
    return crud.retailer_sector.filter(db)


@router.post("/")
async def post_retailer_sector(
    *,
    db: Session = Depends(get_db),
    retailer_sector: RetailerSectorCreate
) -> Any:
    sector = get_sector_by_id(retailer_sector.sector_id)
    if not sector:
        raise HTTPException(
            status_code=400,
            detail=f"The Sector with id '{retailer_sector.sector_id}' does not exists",
        )

    return crud.retailer_sector.create(db, object_to_create=retailer_sector)


@router.get("/{retailer_sector_id}", response_model=RetailerSector)
async def get_retailer_sector_by_id(
    *,
    db: Session = Depends(get_db),
    retailer_sector_id: int,
) -> Any:
    retailer_sector = crud.retailer_sector.get_by_id(db, id=retailer_sector_id)
    if not retailer_sector:
        raise HTTPException(
            status_code=404, detail="The retailer_sector doesn't exists"
        )
    return retailer_sector


@router.put("/{retailer_sector_id}", response_model=RetailerSector)
def update_retailer_sector(
    *,
    db: Session = Depends(get_db),
    retailer_sector_id: int,
    retailer_sector_update: RetailerSectorUpdate,
) -> Any:
    retailer_sector = crud.retailer_sector.get_by_id(db, id=retailer_sector_id)
    if not retailer_sector:
        raise HTTPException(
            status_code=404,
            detail="The retailer_sector doesn't exists",
        )
    retailer_sector = crud.retailer_sector.update(db, db_object=retailer_sector,
                                          object_to_update=retailer_sector_update)
    return retailer_sector


@router.delete("/{retailer_sector_id}", response_model=RetailerSector)
def delete_retailer_sector(
    *,
    db: Session = Depends(get_db),
    retailer_sector_id: int,
) -> Any:
    retailer_sector = crud.retailer_sector.get_by_id(db=db, id=retailer_sector_id)
    if not retailer_sector:
        raise HTTPException(status_code=404, detail="RetailerSector not found")
    retailer_sector = crud.retailer_sector.remove(db=db, id=retailer_sector_id)
    return retailer_sector
