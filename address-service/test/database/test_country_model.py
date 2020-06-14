from sqlalchemy.orm import Session

from database.crud import country as crud
from database.schema import CountryCreate


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
