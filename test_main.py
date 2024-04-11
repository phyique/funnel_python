from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_response():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {'data': {'average': 0.0, 'message': 'WARNING: RAPID ORBITAL DECAY IMMINENT'}}


def test_stats():
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert (data['data']['maximum'] > 0)


def test_health_altitude():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data['data']['average'] == 1


def test_health_message():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert (data['data']['message'] == 'Sustained Low Earth Orbit Resumed' or
            data['data']['message'] == 'Altitude is A-OK')
