from sqlalchemy.orm import Session

from database.crud import country as crud
from database.schema import CountryCreate, CountryUpdate


def test_list_all_countries(db: Session) -> None:
    countries = crud.filter(db)
    assert countries == []
    assert len(countries) == 0
    new_country = CountryCreate(name="Ecuador", code="EC", language="ES", currency="USD")
    crud.create(db, new_country)
    countries = crud.filter(db)
    assert len(countries) == 1


def test_create_country(db: Session) -> None:
    name = "Chile"
    code = "CH"
    language = "ES"
    currency = "PC"
    country_create = CountryCreate(name=name, code=code, language=language, currency=currency)
    country = crud.create(db, country_create)
    country_created = crud.getById(db, country.id)
    assert country.id == country_created.id
    assert country.code == country_created.code
    assert country.language == country_created.language


def test_update_country(db: Session) -> None:
    country_from_db = crud.getById(db, 2)
    country_update = CountryUpdate(currency="USD")
    updated_country = crud.update(db, db_object=country_from_db, object_to_update=country_update)
    country_from_db = crud.getById(db, 2)
    assert country_from_db.id == updated_country.id
    assert country_from_db.currency == "USD"


def test_delete_country(db: Session) -> None:
    country_from_db = crud.getById(db, 2)
    assert country_from_db
    deleted = crud.remove(db, id=2)
    country_from_db = crud.getById(db, 2)
    assert country_from_db is None
    assert deleted.id == 2
