from sqlalchemy.orm import Session

from database.crud import country as crud
from database.crud import province as province_crud
from database.schema import ProvinceCreate, ProvinceUpdate
from database import models
from test.util.province_util import insert_province


def test_list_all_provinces(db: Session) -> None:
    province_count = province_crud.count(db)
    provinces = province_crud.filter(db)
    assert len(provinces) == province_count
    
    created = insert_province(db)
    countries = province_crud.filter(db)
    assert len(countries) == province_count + 1

    crud.remove(db, id=created.country_id)
    province_crud.remove(db, id=created.id)


def test_create_province(db: Session) -> None:
    created = insert_province(db)
    province_created = province_crud.get_by_id(db, created.id)
    assert created.id == province_created.id
    assert created.name == province_created.name
    assert created.region == province_created.region
    
    crud.remove(db, id=created.country_id)
    province_crud.remove(db, id=created.id)


def test_update_province(db: Session) -> None:
    created = insert_province(db)
    province_from_db = province_crud.get_by_id(db, created.id)
    province_update = ProvinceUpdate(name="Updated")
    updated_province = province_crud.update(db, db_object=province_from_db, object_to_update=province_update)
    province_from_db = province_crud.get_by_id(db, created.id)
    assert province_from_db.id == updated_province.id
    assert province_from_db.name == "Updated"

    crud.remove(db, id=created.country_id)
    province_crud.remove(db, id=created.id)


def test_delete_province(db: Session) -> None:
    created = insert_province(db)
    province_from_db = province_crud.get_by_id(db, created.id)
    assert province_from_db
    deleted = province_crud.remove(db, id=created.id)
    province_from_db = province_crud.get_by_id(db, created.id)
    assert province_from_db is None
    assert deleted.id == created.id

    crud.remove(db, id=created.country_id)
