import requests
import time
from datetime import datetime
from tests.conftest import BASE_URL, register_and_login

def test_health_endpoint_returns_healthy():
    response = requests.get(f"{BASE_URL}/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_user_creates_new_user():
    username = f"test_user{str(time.time())}"
    response = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": username,
        "password": "test_password"
    })
    assert response.status_code == 201
    assert response.json()["user"]["username"] == username

def test_login_returns_jwt_token():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "test_user1779134132.726491",
        "password": "test_password"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_public_event_requires_auth_and_succeeds_with_token(register_and_login):
    date = datetime.now().isoformat()

    response = requests.post(f"{BASE_URL}/api/events", json={
        "title": "test_title",
        "date": date,
        "description": "test_description"
    }, headers={"Authorization": f"Bearer {register_and_login}"})

    assert response.status_code == 201
    assert response.json()["title"] == "test_title"
    assert response.json()["date"] == date
    assert response.json()["description"] == "test_description"

def test_register_to_public_event(register_and_login):
    response = requests.post(f"{BASE_URL}/api/rsvps/event/1",
                             json={"attending": True},
                             headers={"Authorization": f"Bearer {register_and_login}"})

    assert response.status_code == 201
    assert response.json()["attending"] == True

def test_double_registration():
    username = f"test_user{str(time.time())}"
    first_registration = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": username,
        "password": "test_password"
    })

    second_registration = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": username,
        "password": "test_password"
    })

    assert first_registration.status_code == 201
    assert second_registration.status_code == 400

def test_create_public_event_without_auth():
    date = datetime.now().isoformat()

    response = requests.post(f"{BASE_URL}/api/events", json={
        "title": "test_title",
        "date": date,
        "description": "test_description"
    })

    assert response.status_code == 401
    assert response.json()["msg"] == "Missing Authorization Header"

def test_rsvp_not_public_event_and_without_auth(register_and_login):
    date = datetime.now().isoformat()

    response = requests.post(f"{BASE_URL}/api/events", json={
        "title": "test_title",
        "date": date,
        "description": "test_description",
        "is_public": False,
    }, headers={"Authorization": f"Bearer {register_and_login}"})

    event_id = response.json()["id"]

    response_rsvp = requests.post(f"{BASE_URL}/api/rsvps/event/{event_id}",
                                  json={"attending": True})

    assert response_rsvp.status_code == 401
    assert response_rsvp.json()["error"] == "Authentication required for this event"