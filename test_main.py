from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


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
    main.cache = [
        {'altitude': 132.91778679216426, 'last_updated': '2024-04-11T08:35:50', 'time_lapse': 0.2833333333333333},
        {'altitude': 133.84594580188326, 'last_updated': '2024-04-11T08:36:00', 'time_lapse': 0.11666666666666667},
        {'altitude': 133.84594580188326, 'last_updated': '2024-04-11T08:36:00', 'time_lapse': 0.11666666666666667}]
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data['data']['average'] == 133.53655946531026


def test_health_message():
    main.cache = [{'altitude': 161.91778679216426, 'last_updated': '2024-04-11T08:35:50', 'time_lapse': 0.2},
                  {'altitude': 180.84594580188326, 'last_updated': '2024-04-11T08:36:00',
                   'time_lapse': 0.03333333333333333}]
    main.sustained = False
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data['data']['message'] == 'Sustained Low Earth Orbit Resumed'


def test_health_ok():
    main.cache = [{'altitude': 161.91778679216426, 'last_updated': '2024-04-11T08:35:50', 'time_lapse': 0.2},
                  {'altitude': 180.84594580188326, 'last_updated': '2024-04-11T08:36:00',
                   'time_lapse': 0.03333333333333333}]
    main.sustained = True
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data['data']['message'] == 'Altitude is A-OK'
