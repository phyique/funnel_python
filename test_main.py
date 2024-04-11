from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_response():
    response = client.get("/api/health/")
    assert response.status_code == 200
    assert response.json() == {'data': {'average': 0.0, 'message': 'WARNING: RAPID ORBITAL DECAY IMMINENT'}}