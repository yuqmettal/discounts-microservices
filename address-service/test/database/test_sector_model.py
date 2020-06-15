from sqlalchemy.orm import Session

from database import crud
from database.schema.sector_schema import SectorCreate, SectorUpdate
from database import models
from test.util.sector_util import insert_sector, delete_sector
from test.util.city_util import delete_city_by_id


def test_list_all_sectors(db: Session) -> None:
    sector_count = crud.sector.count(db)
    sectors = crud.sector.filter(db)
    assert len(sectors) == sector_count
    
    created = insert_sector(db)
    sectors = crud.sector.filter(db)
    assert len(sectors) == sector_count + 1

    delete_sector(db, created)


def test_create_sector(db: Session) -> None:
    created = insert_sector(db)
    sector_created = crud.sector.get_by_id(db, created.id)
    assert created.id == sector_created.id
    assert created.name == sector_created.name
    
    delete_sector(db, created)


def test_update_sector(db: Session) -> None:
    created = insert_sector(db)
    sector_from_db = crud.sector.get_by_id(db, created.id)
    sector_update = SectorUpdate(name="Updated")
    updated_sector = crud.sector.update(db, db_object=sector_from_db, object_to_update=sector_update)
    sector_from_db = crud.sector.get_by_id(db, created.id)
    assert sector_from_db.id == updated_sector.id
    assert sector_from_db.name == "Updated"

    delete_sector(db, created)


def test_delete_sector(db: Session) -> None:
    created = insert_sector(db)
    sector_from_db = crud.sector.get_by_id(db, created.id)
    assert sector_from_db
    deleted = crud.sector.remove(db, id=created.id)
    sector_from_db = crud.sector.get_by_id(db, created.id)
    assert sector_from_db is None
    assert deleted.id == created.id

    delete_city_by_id(db, deleted.city_id)
