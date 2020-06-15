from sqlalchemy.orm import Session

from database.schema.sector_schema import SectorCreate, SectorUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import Sector
from .city_util import insert_city, delete_city


def create_random_sector(city_id: int) -> SectorCreate:
    name = random_lower_string()
    return SectorCreate(name=name, city_id=city_id)


def create_random_sector_data(city_id: int):
    name = random_lower_string()
    return {'name': name, 'city_id': city_id}


def insert_sector(db: Session):
    city = insert_city(db)
    sector_create = create_random_sector(city.id)
    return crud.sector.create(db, sector_create)


def delete_sector(db: Session, sector: Sector):
    city = crud.city.get_by_id(db, id=sector.city_id)
    province = crud.province.get_by_id(db, id=city.province_id)
    crud.sector.remove(db, id=sector.id)
    crud.city.remove(db, id=city.id)
    crud.province.remove(db, id=city.province_id)
    crud.country.remove(db, id=province.country_id)
