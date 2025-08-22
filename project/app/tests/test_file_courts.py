import os
import json
import requests
from dotenv import load_dotenv

import pytest

load_dotenv()

headers = {"Content-Type": "application/json"}
admin_credentials = json.loads(os.getenv("admin_credentails"))
court_credentials_1 = json.loads(os.getenv("court_credentials_1"))
court_credentials_2 = json.loads(os.getenv("court_credentials_2"))


BASE_URL = os.getenv("adress")

courts_url = f"{BASE_URL}/courts"

session = requests.session()

res = session.post(f"{BASE_URL}/login", json=admin_credentials, headers=headers)

@pytest.fixture()
def court_setup():

    court_post_res = session.post(courts_url, json=court_credentials_1, headers=headers )

    court_id = court_post_res.json().get("id")

    yield court_id

    session.delete(f"{courts_url}/{court_id}")


def test_get_courts_200(court_setup):

    get_res = session.get(courts_url)

    assert get_res.status_code == 200


def test_get_court_200(court_setup):

    court_id = court_setup

    get_res = session.get(f"{courts_url}/{court_id}")

    assert get_res.status_code == 200


def test_get_court_404(court_setup):

    court_id = court_setup

    session.delete(f"{courts_url}/{court_id}")

    get_res = session.get(f"{courts_url}/{court_id}")

    assert get_res.status_code == 404


def test_post_court_201():

    post_res = session.post(courts_url, json=court_credentials_1, headers=headers)

    court_id = post_res.json().get("id")

    assert post_res.status_code == 201

    session.delete(f"{courts_url}/{court_id}")


def test_post_court_400():

    post_res = session.post(courts_url, json={}, headers=headers)

    assert post_res.status_code == 400


def test_post_court_422():

    data = court_credentials_1.copy()

    data.pop("location")

    post_res = session.post(courts_url, json=data, headers=headers)

    assert post_res.status_code == 422


def test_post_court_409(court_setup):

    court_id_1 = court_setup

    post_res_2 = session.post(courts_url, json=court_credentials_1, headers=headers)

    assert post_res_2.status_code == 409

def test_put_court_400(court_setup):

    court_id = court_setup

    put_res = session.put(f"{courts_url}/{court_id}", json={}, headers=headers)

    assert put_res.status_code == 400


def test_put_court_409(court_setup):

    post_res_2 = session.post(courts_url, json=court_credentials_2, headers=headers)

    court_id_2 = post_res_2.json().get("id")
    
    put_res = session.put(f"{courts_url}/{court_id_2}", json=court_credentials_1, headers=headers)

    assert put_res.status_code == 409

    session.delete(f"{courts_url}/{court_id_2}")


def test_put_court_200(court_setup):

    court_id = court_setup

    put_res = session.put(f"{courts_url}/{court_id}", json=court_credentials_2, headers=headers)

    assert put_res.status_code == 200


def test_delete_court_200(court_setup):

    court_id = court_setup
    
    delete_res = session.delete(f"{courts_url}/{court_id}")

    assert delete_res.status_code == 200




