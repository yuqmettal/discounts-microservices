import os
import json

import settings
from database import crud, SessionLocal
from database.schema.brand_schema import BrandCreate
from database.schema.product_schema import ProductCreate


def seed_data():
    seed_brand_data()
    seed_product_data()


def seed_brand_data():
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'brands.json'
    )
    with open(json_file) as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for brand_data in data:
            brand = crud.brand.get_by_id(db=db, id=brand_data['id'])
            if not brand:
                brand = BrandCreate(**brand_data)
                crud.brand.create(db, object_to_create=brand)


def seed_product_data():
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'products.json'
    )
    with open(json_file) as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for product_data in data:
            product = crud.product.get_by_id(db=db, id=product_data['id'])
            if not product:
                product = ProductCreate(**product_data)
                crud.product.create(db, object_to_create=product)
