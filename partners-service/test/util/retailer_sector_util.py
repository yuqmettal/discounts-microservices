from sqlalchemy.orm import Session

from database.schema.retailer_sector_schema import RetailerSectorCreate
from database import crud
from database.models import RetailerSector


def create_random_retailer_sector() -> RetailerSectorCreate:
    sector_id = 1
    retailer_id = 1
    enabled = True
    return RetailerSectorCreate(sector_id=sector_id, retailer_id=retailer_id, enabled=enabled)


def create_random_retailer_sector_data():
    sector_id = 1
    retailer_id = 1
    enabled = True
    return {'sector_id': sector_id, 'retailer_id': retailer_id, 'enabled': enabled}


def insert_retailer_sector(db: Session):
    retailer_sector_create = create_random_retailer_sector()
    return crud.retailer_sector.create(db, retailer_sector_create)


def delete_retailer_sector(db: Session, retailer_sector: RetailerSector):
    crud.retailer_sector.remove(db, id=retailer_sector.id)
