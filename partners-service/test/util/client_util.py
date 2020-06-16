from sqlalchemy.orm import Session

from database.schema.client_schema import ClientCreate, ClientUpdate
from .utils import random_lower_string, random_upper_string, random_email
from database import crud
from database.models import Client


def create_random_client() -> ClientCreate:
    name = random_lower_string()
    last_name = random_lower_string()
    email = random_email()
    return ClientCreate(name=name, last_name=last_name, email=email)


def create_random_client_data():
    name = random_lower_string()
    last_name = random_lower_string()
    email = random_email()
    return {'name': name, 'last_name': last_name, 'email': email}


def insert_client(db: Session):
    client_create = create_random_client()
    return crud.client.create(db, client_create)


def delete_client(db: Session, client: Client):
    crud.client.remove(db, id=client.id)
