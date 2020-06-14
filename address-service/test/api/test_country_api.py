from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database.crud import country as crud
from database.schema import CountryCreate
from test.util.country_util import create_random_country


client = TestClient(app)


def test_GET_countries(db: Session) -> None:
    country_count = crud.count(db)
    response = client.get('/api/v1/country')
    assert response.status_code == 200
    assert len(response.json()) == country_count
    new_country = create_random_country()
    created = crud.create(db, object_to_create=new_country)

    response = client.get('/api/v1/country')
    assert response.status_code == 200
    assert len(response.json()) == country_count + 1
    crud.remove(db, id=created.id)