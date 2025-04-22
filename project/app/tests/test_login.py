import subprocess
import time
import pytest
import requests

BASE_URL = "http://192.168.0.66:5000"
USERS_URL= "/users"
LOGIN_URL = "/login"

def create_payload():
    return {
        "name": "testuser",
        "email": "test@example.com",
        "password": "securepassword"
    }

def post_request(payload=create_payload(), endpoint=USERS_URL):

    response = requests.post(f"{BASE_URL}/{endpoint}", json=payload)

    return response

def wait_for_api(timeout=15):
    for _ in range(timeout):
        try:
            response = requests.get(f"{BASE_URL}/login")  # or your health endpoint
            if response.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    raise RuntimeError("API did not become ready in time.")


@pytest.fixture(scope="session", autouse=True)
def docker_setup_and_teardown():
    print("🚀 Starting Docker containers...")
    subprocess.run(["docker-compose", "-f", "docker-compose-test.yml", "up", "--build", "-d"], check=True)
    try:
        wait_for_api()
        requests.post(f"{BASE_URL}/{USERS_URL}", json=create_payload())
        yield
    finally:
        print("🧹 Shutting down and removing containers/volumes...")
        subprocess.run(["docker-compose", "down", "--volumes", "--rmi", "all", "--remove-orphans"
], check=True)


def test_invalid_input():
    payload = create_payload()
    payload.pop("name")
    payload.update({"password": "password"})
    
    response = post_request(payload=payload, endpoint=LOGIN_URL)
    assert response.status_code == 401

def test_login_empty():
    payload = create_payload()
    payload.pop("name")
    payload.pop("email")
    
    response = post_request(payload=payload, endpoint=LOGIN_URL)
    assert response.status_code == 400

def test_login_success():
    payload = create_payload()
    payload.pop("name")

    response = post_request(payload=payload, endpoint=LOGIN_URL)
    assert response.status_code == 200

