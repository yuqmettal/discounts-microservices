from sqlalchemy.orm import Session

from database import crud
from database.schema.retailer_sector_schema import RetailerSectorCreate, RetailerSectorUpdate
from test.util.retailer_sector_util import insert_retailer_sector, delete_retailer_sector


def test_list_all_retailer_sectors(db: Session) -> None:
    retailer_sector_count = crud.retailer_sector.count(db)
    retailer_sectors = crud.retailer_sector.filter(db)
    assert len(retailer_sectors) == retailer_sector_count
    created = insert_retailer_sector(db)
    retailer_sectors = crud.retailer_sector.filter(db)
    assert len(retailer_sectors) == retailer_sector_count + 1
    delete_retailer_sector(db, created)


def test_create_retailer_sector(db: Session) -> None:
    created = insert_retailer_sector(db)
    retailer_sector_created = crud.retailer_sector.get_by_id(db, created.id)
    assert created.id == retailer_sector_created.id
    assert created.retailer_id == retailer_sector_created.retailer_id
    delete_retailer_sector(db, created)


def test_update_retailer_sector(db: Session) -> None:
    created = insert_retailer_sector(db)
    retailer_sector_from_db = crud.retailer_sector.get_by_id(db, created.id)
    retailer_sector_update = RetailerSectorUpdate(enabled=False)
    updated_retailer_sector = crud.retailer_sector.update(
        db, db_object=retailer_sector_from_db, object_to_update=retailer_sector_update)
    retailer_sector_from_db = crud.retailer_sector.get_by_id(db, created.id)
    assert retailer_sector_from_db.id == updated_retailer_sector.id
    assert retailer_sector_from_db.enabled == False
    delete_retailer_sector(db, created)


def test_delete_retailer_sector(db: Session) -> None:
    created = insert_retailer_sector(db)

    retailer_sector_from_db = crud.retailer_sector.get_by_id(db, created.id)
    assert retailer_sector_from_db
    deleted = crud.retailer_sector.remove(db, id=created.id)
    retailer_sector_from_db = crud.retailer_sector.get_by_id(db, created.id)
    assert retailer_sector_from_db is None
    assert deleted.id == created.id
