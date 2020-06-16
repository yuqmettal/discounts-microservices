from sqlalchemy.orm import Session

from database.schema.product_schema import ProductCreate, ProductUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import Product


def create_random_product() -> ProductCreate:
    name = random_lower_string()
    description = random_lower_string()
    tax_rate = 12
    brand_id = 1
    return ProductCreate(name=name, description=description, tax_rate=tax_rate, brand_id=brand_id)


def create_random_product_data():
    name = random_lower_string()
    description = random_lower_string()
    tax_rate = 12
    brand_id = 1
    return {'name': name, 'description': description, 'tax_rate': tax_rate, 'brand_id': brand_id}


def insert_product(db: Session):
    product_create = create_random_product()
    return crud.product.create(db, product_create)


def delete_product(db: Session, product: Product):
    crud.product.remove(db, id=product.id)
