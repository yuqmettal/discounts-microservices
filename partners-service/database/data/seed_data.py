import os
import json
import logging

logger = logging.getLogger(__name__)

import settings
from database import crud, SessionLocal
from database.schema.category_schema import CategoryCreate
from database.schema.subcategory_schema import SubcategoryCreate
from database.schema.retailer_schema import RetailerCreate
from database.schema.prime_subscription_schema import PrimeSubscriptionCreate
from database.schema.client_schema import ClientCreate
from database.schema.retailer_category_schema import RetailerCategoryCreate
from database.schema.retailer_sector_schema import RetailerSectorCreate
from database.schema.client_prime_subscription_schema import ClientPrimeSubscriptionCreate


def seed_data():
    seed_category_data()
    seed_subcategory_data()
    seed_retailer_data()
    seed_prime_subscription_data()
    seed_client_data()
    seed_retailer_category_data()
    seed_retailer_sector_data()
    seed_client_prime_data()


def seed_category_data():
    logger.info("Seeding categories")
    db = SessionLocal()
    if crud.category.count(db) > 0:
        return
    category_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'categories.json'
    )
    with open(category_file) as json_file:
        data = json.load(json_file)
        for category_data in data:
            category = CategoryCreate(**category_data)
            crud.category.create(db, object_to_create=category)


def seed_subcategory_data():
    logger.info("Seeding subcategories")
    db = SessionLocal()
    if crud.subcategory.count(db) > 0:
        return
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'subcategories.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        for subcategory_data in data:
            subcategory = SubcategoryCreate(**subcategory_data)
            crud.subcategory.create(db, object_to_create=subcategory)


def seed_retailer_data():
    logger.info("Seeding retailers")
    db = SessionLocal()
    if crud.retailer.count(db) > 0:
        return
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'retailers.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        for retailer_data in data:
            retailer = RetailerCreate(**retailer_data)
            crud.retailer.create(db, object_to_create=retailer)


def seed_prime_subscription_data():
    logger.info("Seeding prime subscriptions")
    db = SessionLocal()
    if crud.prime_subscription.count(db) > 0:
        return
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'prime_subscriptions.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        for prime_subscription_data in data:
            prime_subscription = PrimeSubscriptionCreate(**prime_subscription_data)
            crud.prime_subscription.create(db, object_to_create=prime_subscription)


def seed_client_data():
    logger.info("Seeding clients")
    db = SessionLocal()
    if crud.client.count(db) > 0:
        return
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'clients.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        for client_data in data:
            client = ClientCreate(**client_data)
            crud.client.create(db, object_to_create=client)


def seed_retailer_category_data():
    logger.info("Seeding retailer categories")
    db = SessionLocal()
    if crud.retailer_category.count(db) > 0:
        return
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'retailer_categories.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        for retailer_category_data in data:
            retailer_category = RetailerCategoryCreate(**retailer_category_data)
            crud.retailer_category.create(db, object_to_create=retailer_category)


def seed_retailer_sector_data():
    logger.info("Seeding retailer sectors")
    db = SessionLocal()
    if crud.retailer_sector.count(db) > 0:
        return
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'retailer_sectors.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        for retailer_sector_data in data:
            retailer_sector = RetailerSectorCreate(**retailer_sector_data)
            crud.retailer_sector.create(db, object_to_create=retailer_sector)


def seed_client_prime_data():
    logger.info("Seeding client prime subscriptions")
    db = SessionLocal()
    if crud.client_prime_subscription.count(db) > 0:
        return
    json_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'client_prime_subscriptions.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        for client_prime_data in data:
            client_prime = ClientPrimeSubscriptionCreate(**client_prime_data)
            crud.client_prime_subscription.create(db, object_to_create=client_prime)
