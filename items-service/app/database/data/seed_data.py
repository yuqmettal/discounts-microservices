import os
import json
import logging

logger = logging.getLogger(__name__)

import settings
from app.database import crud, SessionLocal
from app.database.schema.brand_schema import BrandCreate
from app.database.schema.product_schema import ProductCreate
from app.database.schema.item_schema import ItemCreate
from app.database.schema.discount_schema import DiscountCreate


def seed_data():
    seed_brand_data()
    seed_product_data()
    seed_item_data()
    seed_discount_data()


def seed_brand_data():
    logger.info("Seeding brands")
    db = SessionLocal()
    if crud.brand.count(db) > 0:
        return
    json_file = os.path.join(
        settings.BASE_DIR,
        'app',
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
    logger.info("Seeding products")
    db = SessionLocal()
    if crud.product.count(db) > 0:
        return
    json_file = os.path.join(
        settings.BASE_DIR,
        'app',
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
    logger.info("Seeding items")
    db = SessionLocal()
    if crud.item.count(db) > 0:
        return
    json_file = os.path.join(
        settings.BASE_DIR,
        'app',
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
    logger.info("Seeding discounts")
    db = SessionLocal()
    if crud.discount.count(db) > 0:
        return
    json_file = os.path.join(
        settings.BASE_DIR,
        'app',
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
