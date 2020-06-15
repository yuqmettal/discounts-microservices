from sqlalchemy.orm import Session

from database.schema import CountryCreate
from database.schema import ProvinceCreate
from .utils import random_lower_string, random_upper_string
from database.crud import province as crud
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
    return crud.create(db, country_create)