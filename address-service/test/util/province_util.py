from sqlalchemy.orm import Session

from database.schema import CountryCreate, ProvinceCreate
from database.models import Province
from .utils import random_lower_string, random_upper_string
from database import crud
from .country_util import insert_country


def create_random_province(country_id: int) -> ProvinceCreate:
    name = random_lower_string()
    region = random_lower_string()
    return ProvinceCreate(name=name, region=region, country_id=country_id)


def create_random_province_data(country_id: int):
    name = random_lower_string()
    region = random_lower_string()
    return {'name': name, 'region': region, 'country_id': country_id}


def insert_province(db: Session):
    country = insert_country(db)
    country_create = create_random_province(country.id)
    return crud.province.create(db, country_create)


def delete_province(db: Session, province: Province):
    crud.province.remove(db, id=province.id)
    crud.country.remove(db, id=province.country_id)


def delete_province_by_id(db: Session, id: int):
    province = crud.province.get_by_id(db, id=id)
    delete_province(db, province)
