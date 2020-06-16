import os
import json

import settings
from database import crud, SessionLocal
from database.schema.category_schema import CategoryCreate
from database.schema.subcategory_schema import SubcategoryCreate
from database.schema.retailer_schema import RetailerCreate


def seed_data():
    seed_category_data()
    seed_subcategory_data()
    seed_retailer_data()


def seed_category_data():
    category_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'categories.json'
    )
    with open(category_file) as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for category_data in data:
            category = crud.category.get_by_id(db=db, id=category_data['id'])
            if not category:
                category = CategoryCreate(**category_data)
                crud.category.create(db, object_to_create=category)


def seed_subcategory_data():
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'subcategories.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for subcategory_data in data:
            subcategory = crud.subcategory.get_by_id(db=db, id=subcategory_data['id'])
            if not subcategory:
                subcategory = SubcategoryCreate(**subcategory_data)
                crud.subcategory.create(db, object_to_create=subcategory)


def seed_retailer_data():
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'retailers.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for retailer_data in data:
            retailer = crud.retailer.get_by_id(db=db, id=retailer_data['id'])
            if not retailer:
                retailer = RetailerCreate(**retailer_data)
                crud.retailer.create(db, object_to_create=retailer)
