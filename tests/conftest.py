import pytest
import requests
import time

BASE_URL= "http://127.0.0.1:5000"

@pytest.fixture
def register_and_login():
    username = f"test_user{str(time.time())}"
    response_register = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": username,
        "password": "test_password"
    })

    if response_register.status_code == 201:
        response_login = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "username": username,
                "password": "test_password"
            }
        )
        return response_login.json()["access_token"]
    else:
        return None

@pytest.fixture
def auth_token():
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "username": "test_user1779134132.726491",
            "password": "test_password"
        }
    )

    return response.json()["access_token"]