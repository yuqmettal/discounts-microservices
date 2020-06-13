from fastapi.testclient import TestClient
from unittest import mock

from main import app
from database.models import Country


client = TestClient(app)


@mock.patch('database.models.Country')
def test_list_all_countries(mocked_country):
    mocked_country.query.all.return_value = []
    
    response = client.get("api/v1/country")
    assert response.status_code == 200
    assert response.json() == []