from sqlalchemy.orm import Session

from database.crud import country
from database.schema import CountryCreate


def test_list_all_countries(db: Session) -> None:
    countries = country.filter(db)
    assert countries == []
    assert len(countries) == 0
    new_country = CountryCreate(name="Ecuador", code="EC", language="ES", currency="USD")
    country.create(db, new_country)
    countries = country.filter(db)
    assert len(countries) == 1
