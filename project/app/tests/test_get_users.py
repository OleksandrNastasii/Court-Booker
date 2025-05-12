import subprocess
import time
import pytest
import requests

BASE_URL = "http://192.168.0.66:5000"

def create_payload():
    return {
        "name": "testuser",
        "email": "test@example.com",
        "password": "securepassword"
    }

def post_request(payload=create_payload()):

    response = requests.post(f"{BASE_URL}/users", json=payload)

    return response

def get_request():
    response = requests.get(f"{BASE_URL}/users")

    return response

def wait_for_api(timeout=15):
    for _ in range(timeout):
        try:
            response = requests.get(f"{BASE_URL}/users")
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
        yield
    finally:
        print("🧹 Shutting down and removing containers/volumes...")
        subprocess.run(["docker-compose", "down", "--volumes", "--rmi", "all", "--remove-orphans"
], check=True)
        
def test_no_users():
    response = get_request()

    assert response.status_code == 200

def test_get_all_users():
    post_request()
    response = get_request()

    assert response.status_code == 200