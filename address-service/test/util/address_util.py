from sqlalchemy.orm import Session

from database.schema.address_schema import AddressCreate, AddressUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import Address
from .city_util import insert_city, delete_city


def create_random_address() -> AddressCreate:
    name = random_lower_string()
    line_one = random_lower_string()
    line_two = random_lower_string()
    return AddressCreate(name=name, sector_id=1, line_one=line_one, line_two=line_two)


def create_random_address_data():
    name = random_lower_string()
    line_one = random_lower_string()
    line_two = random_lower_string()
    return {'name': name, 'sector_id': 1, 'line_one': line_one, 'line_two': line_two}


def insert_address(db: Session):
    address_create = create_random_address()
    return crud.address.create(db, address_create)


def delete_address(db: Session, address: Address):
    crud.address.remove(db, id=address.id)
