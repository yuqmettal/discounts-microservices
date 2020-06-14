from sqlalchemy.orm import Session

from database.crud import country as crud
from database.schema import CountryCreate, CountryUpdate
from database import models
from test.util.country_util import create_random_country


def test_list_all_countries(db: Session) -> None:
    country_count = crud.count(db)
    countries = crud.filter(db)
    assert len(countries) == country_count
    new_country = create_random_country()
    created = crud.create(db, new_country)
    countries = crud.filter(db)
    assert len(countries) == country_count + 1
    crud.remove(db, id=created.id)


def test_create_country(db: Session) -> None:
    country_create = create_random_country()
    created = crud.create(db, country_create)
    country_created = crud.get_by_id(db, created.id)
    assert created.id == country_created.id
    assert created.code == country_created.code
    assert created.language == country_created.language
    crud.remove(db, id=created.id)


def test_update_country(db: Session) -> None:
    country_create = create_random_country()
    created = crud.create(db, country_create)

    country_from_db = crud.get_by_id(db, created.id)
    country_update = CountryUpdate(currency="USD")
    updated_country = crud.update(db, db_object=country_from_db, object_to_update=country_update)
    country_from_db = crud.get_by_id(db, created.id)
    assert country_from_db.id == updated_country.id
    assert country_from_db.currency == "USD"

    crud.remove(db, id=created.id)


def test_delete_country(db: Session) -> None:
    country_create = create_random_country()
    created = crud.create(db, country_create)

    country_from_db = crud.get_by_id(db, created.id)
    assert country_from_db
    deleted = crud.remove(db, id=created.id)
    country_from_db = crud.get_by_id(db, created.id)
    assert country_from_db is None
    assert deleted.id == created.id
