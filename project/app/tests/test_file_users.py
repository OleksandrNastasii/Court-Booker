import os
import json
import requests
import pytest
from dotenv import load_dotenv

load_dotenv()

headers = {"Content-Type": "application/json"}
admin_credentials = json.loads(os.environ["admin_credentials"])
user_credentials_1 = json.loads(os.environ["user_credentails_1"])
user_credentials_2 = json.loads(os.environ["user_credentails_2"])


BASE_URL = os.environ["adress"]

users_url = f"{BASE_URL}/users"

session = requests.session()

res = session.post(f"{BASE_URL}/login", json=admin_credentials, headers=headers)


@pytest.fixture
def user_setup():

    post_res = session.post(users_url, json=user_credentials_1, headers=headers).json()

    user_id = post_res.get("id")

    yield user_id

    session.delete(f"{users_url}/{user_id}")


#Tests for get request
def test_get_all_users_200(user_setup):

    get_res = session.get(users_url)
    assert get_res.status_code == 200

def test_get_user_200(user_setup):

    user_id = user_setup

    get_res = session.get(f"{users_url}/{user_id}")

    assert get_res.status_code == 200

def test_get_user_404(user_setup):

    user_id = user_setup

    session.delete(f"{users_url}/{user_id}")

    get_res = session.get(f"{users_url}/{user_id}")

    assert get_res.status_code == 404

# #Tests for post requests
def test_post_user_201():

    post_res = session.post(users_url, json=user_credentials_1, headers=headers)

    assert post_res.status_code == 201

    user_id = post_res.json().get("id")
    
    session.delete(f"{users_url}/{user_id}")


def test_post_user_409(user_setup):

    post_res = session.post(users_url, json=user_credentials_1, headers=headers)

    assert post_res.status_code == 409


def test_post_user_422():

    data = user_credentials_1.copy()

    data.pop("name")

    post_res = session.post(users_url, json=data, headers=headers)

    assert post_res.status_code == 422

    user_id = post_res.json().get("id")

    session.delete(f"{users_url}/{user_id}")


# #Tests for put request
def test_put_user_200(user_setup):

    user_id = user_setup

    put_res = session.put(f"{users_url}/{user_id}", json=user_credentials_2, headers=headers)

    assert put_res.status_code == 200


def test_put_user_400(user_setup):

    user_id = user_setup

    put_res = session.put(f"{users_url}/{user_id}", json={}, headers=headers)

    assert put_res.status_code == 400


def test_put_user_409(user_setup):

    post_res_2 = session.post(users_url, json=user_credentials_2, headers=headers)

    user_id_2 = post_res_2.json().get("id")

    put_res = session.put(f"{users_url}/{user_id_2}", json=user_credentials_1, headers=headers)

    assert put_res.status_code == 409

    session.delete(f"{users_url}/{user_id_2}")


# #Test for delete requests
def test_delete_user_200():
    
    post_res = session.post(users_url, json=user_credentials_1, headers=headers)

    user_id = post_res.json().get("id")

    delete_res = session.delete(f"{users_url}/{user_id}")

    assert delete_res.status_code == 200
    




    



