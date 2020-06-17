import os
import json

import settings
from database import crud, SessionLocal
from database.schema.brand_schema import BrandCreate
from database.schema.product_schema import ProductCreate
from database.schema.item_schema import ItemCreate
from database.schema.discount_schema import DiscountCreate


def seed_data():
    seed_brand_data()
    seed_product_data()
    seed_item_data()
    seed_discount_data()


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


def seed_item_data():
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'items.json'
    )
    with open(json_file) as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for item_data in data:
            item = crud.item.get_by_id(db=db, id=item_data['id'])
            if not item:
                item = ItemCreate(**item_data)
                crud.item.create(db, object_to_create=item)


def seed_discount_data():
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'discounts.json'
    )
    with open(json_file) as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for discounts_data in data:
            discount = crud.discount.get_by_id(db=db, id=discounts_data['id'])
            if not discount:
                discount = DiscountCreate(**discounts_data)
                crud.discount.create(db, object_to_create=discount)
