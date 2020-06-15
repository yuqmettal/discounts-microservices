from sqlalchemy.orm import Session

from database.schema.city_schema import CityCreate, CityUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import City
from .province_util import insert_province, insert_country


def create_random_city(province_id: int) -> CityCreate:
    name = random_lower_string()
    return CityCreate(name=name, province_id=province_id)


def create_random_city_data(province_id: int):
    name = random_lower_string()
    return {'name': name, 'province_id': province_id}


def insert_city(db: Session):
    province = insert_province(db)
    city_create = create_random_city(province.id)
    return crud.city.create(db, city_create)


def delete_city(db: Session, city: City):
    province = crud.province.get_by_id(db, id=city.province_id)
    crud.city.remove(db, id=city.id)
    crud.province.remove(db, id=city.province_id)
    crud.country.remove(db, id=province.country_id)


def delete_city_by_id(db: Session, id: int):
    city = crud.city.get_by_id(db, id=id)
    delete_city(db, city)
