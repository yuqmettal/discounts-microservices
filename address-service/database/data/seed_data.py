import os
import json

from fastapi import Depends
from sqlalchemy.orm import Session

import settings
from database import crud, SessionLocal
from api import get_db
from database.schema.country_schema import CountryInsert
from database.schema.province_schema import ProvinceInsert
from database.schema.city_schema import CityInsert
from database.schema.sector_schema import SectorInsert


def seed_data():
    seed_country_data()
    seed_province_data()
    seed_city_data()
    seed_sector_data()


def seed_country_data():
    country_file = os.path.join(
        settings.BASE_DIR,
        'address-service',
        'database',
        'data',
        'countries.json'
    )
    with open(country_file) as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for country_data in data:
            country = crud.country.get_by_id(db=db, id=country_data['id'])
            if not country:
                country = CountryInsert(**country_data)
                crud.country.create(db, object_to_create=country)


def seed_province_data():
    json_file = os.path.join(
        settings.BASE_DIR,
        'address-service',
        'database',
        'data',
        'provinces.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for province_data in data:
            province = crud.province.get_by_id(db=db, id=province_data['id'])
            if not province:
                province = ProvinceInsert(**province_data)
                crud.province.create(db, object_to_create=province)


def seed_city_data():
    json_file = os.path.join(
        settings.BASE_DIR,
        'address-service',
        'database',
        'data',
        'cities.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for city_data in data:
            city = crud.city.get_by_id(db=db, id=city_data['id'])
            if not city:
                city = CityInsert(**city_data)
                crud.city.create(db, object_to_create=city)


def seed_sector_data():
    json_file = os.path.join(
        settings.BASE_DIR,
        'address-service',
        'database',
        'data',
        'sectors.json'
    )
    with open(json_file, encoding='utf8') as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for sector_data in data:
            sector = crud.sector.get_by_id(db=db, id=sector_data['id'])
            if not sector:
                sector = SectorInsert(**sector_data)
                crud.sector.create(db, object_to_create=sector)
