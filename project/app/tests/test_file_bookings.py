import os
import pytest
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.tests.test_file_courts import courts_url, court_credentials_1

load_dotenv()

headers = {"Content-Type": "application/json"}
admin_credentials = json.loads(os.environ["admin_credentials"])

BASE_URL = os.environ["adress"]

bookings_url = f"{BASE_URL}/bookings"

session = requests.session()

res = session.post(f"{BASE_URL}/login", json=admin_credentials, headers=headers)


@pytest.fixture
def create_court():

    court_post_res = session.post(courts_url, json=court_credentials_1, headers=headers)

    court_id = court_post_res.json().get("id")

    yield court_id

    session.delete(f"{courts_url}/{court_id}")


@pytest.fixture(autouse=True)
def booking_data(create_court):

    now = datetime.now()
    now_plus_one_hour = now + timedelta(hours=1)
    start_time = now_plus_one_hour.replace(microsecond=0).isoformat()
    now_plus_two_hours = now + timedelta(hours=2)
    end_time = now_plus_two_hours.replace(microsecond=0).isoformat()

    user_id = res.json().get("id")

    booking_credentials = { "user_id":user_id,
                            "court_id":f"{create_court}",
                            "start_time":f"{start_time}",
                            "end_time":f"{end_time}"
                      }

    return booking_credentials


def create_booking(booking_data):

    data = booking_data
    
    book_post_res = session.post(bookings_url, json=data, headers=headers)

    return book_post_res

@pytest.fixture()
def setup_teardown(booking_data):


    data = booking_data

    book_post_res = create_booking(data)
    
    booking_id = book_post_res.headers.get("X-Booking-ID")

    yield booking_id

    session.delete(f"{bookings_url}/{booking_id}")


def test_post_booking_400():

    data = {}

    book_post_res = create_booking(data)

    assert book_post_res.status_code == 400


def test_post_booking_422_missed_field(booking_data):

    data = booking_data.copy()

    data.pop("start_time")

    book_post_res = create_booking(data)

    assert book_post_res.status_code == 422


def test_post_booking_422_invalid_format(booking_data):

    data = booking_data.copy()

    data["start_time"] = "string"

    book_post_res = create_booking(data)

    assert book_post_res.status_code == 422


def test_post_booking_422_start_bigger_than_end(booking_data):

    data = booking_data.copy()

    start_time = data["start_time"]

    not_iso = datetime.fromisoformat(start_time)

    not_iso_plus_3 = not_iso + timedelta(hours=3)

    iso_plus_3 = not_iso_plus_3.isoformat()

    data["start_time"] = iso_plus_3

    book_post_res = create_booking(data)

    assert book_post_res.status_code == 422


def test_post_booking_400_start_time_in_past(booking_data):

    data = booking_data.copy()

    start_time = data["start_time"]

    not_iso = datetime.fromisoformat(start_time)

    not_iso_minus_3 = not_iso - timedelta(hours=3)

    iso_minus_3 = not_iso_minus_3.isoformat()

    data["start_time"] = iso_minus_3

    # print(data)

    book_post_res = create_booking(data)

    assert book_post_res.status_code == 400

def test_get_bokings_200(setup_teardown):

    booking_get_res = session.get(bookings_url)

    assert booking_get_res.status_code == 200


def test_put_booking_404(setup_teardown, booking_data):

    data = booking_data.copy()

    booking_id = setup_teardown

    session.delete(f"{bookings_url}/{booking_id}")

    booking_put_res = session.put(f"{bookings_url}/{booking_id}", json=data, headers=headers)

    assert booking_put_res.status_code == 404


def test_put_booking_400(setup_teardown):

    booking_id = setup_teardown

    booking_put_res = session.put(f"{bookings_url}/{booking_id}", json={}, headers=headers)

    assert booking_put_res.status_code == 400


def test_put_booking_200(setup_teardown, booking_data):

    booking_id = setup_teardown

    data = booking_data.copy()

    data["end_time"] = (datetime.now() + timedelta(hours=8)).isoformat()

    booking_put_res = session.put(f"{bookings_url}/{booking_id}", json=data, headers=headers)

    assert booking_put_res.status_code == 200


def test_get_booking_404(setup_teardown):

    booking_id = setup_teardown

    session.delete(f"{bookings_url}/{booking_id}")

    booking_get_res = session.get(f"{bookings_url}/{booking_id}")

    assert booking_get_res.status_code == 404


def test_get_booking_200(setup_teardown):

    booking_id = setup_teardown

    booking_get_res = session.get(f"{bookings_url}/{booking_id}")

    assert booking_get_res.status_code == 200


def test_delete_booking_404(setup_teardown):

    booking_id = setup_teardown

    session.delete(f"{bookings_url}/{booking_id}")

    booking_delete_res = session.delete(f"{bookings_url}/{booking_id}")

    assert booking_delete_res.status_code == 404

def test_delete_booking_200(setup_teardown):

    booking_id = setup_teardown

    booking_delete_res = session.delete(f"{bookings_url}/{booking_id}")

    assert booking_delete_res.status_code == 200