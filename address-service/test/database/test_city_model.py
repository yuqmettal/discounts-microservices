from sqlalchemy.orm import Session

from database import crud
from database.schema.city_schema import CityCreate, CityUpdate
from database import models
from test.util.city_util import insert_city, delete_city
from test.util.province_util import delete_province_by_id


def test_list_all_cities(db: Session) -> None:
    city_count = crud.city.count(db)
    cities = crud.city.filter(db)
    assert len(cities) == city_count
    
    created = insert_city(db)
    cities = crud.city.filter(db)
    assert len(cities) == city_count + 1

    delete_city(db, created)


def test_create_city(db: Session) -> None:
    created = insert_city(db)
    city_created = crud.city.get_by_id(db, created.id)
    assert created.id == city_created.id
    assert created.name == city_created.name
    
    delete_city(db, created)


def test_update_province(db: Session) -> None:
    created = insert_city(db)
    city_from_db = crud.city.get_by_id(db, created.id)
    city_update = CityUpdate(name="Updated")
    updated_city = crud.city.update(db, db_object=city_from_db, object_to_update=city_update)
    city_from_db = crud.city.get_by_id(db, created.id)
    assert city_from_db.id == updated_city.id
    assert city_from_db.name == "Updated"

    delete_city(db, created)


def test_delete_province(db: Session) -> None:
    created = insert_city(db)
    city_from_db = crud.city.get_by_id(db, created.id)
    assert city_from_db
    deleted = crud.city.remove(db, id=created.id)
    city_from_db = crud.city.get_by_id(db, created.id)
    assert city_from_db is None
    assert deleted.id == created.id

    delete_province_by_id(db, deleted.province_id)
