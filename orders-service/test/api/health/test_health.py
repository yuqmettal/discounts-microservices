from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_info():
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}
