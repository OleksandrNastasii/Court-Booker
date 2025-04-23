import flask
import requests
import time
from datetime import datetime, timezone
from sqlalchemy.orm.exc import DetachedInstanceError


from ..models.user_model import BookingModel
from .database import db_session


def update_booking_status():
    while True:
        now = datetime.now(timezone.utc)
        bookings = BookingModel.query.all()

        for booking in bookings:
            booking_id = booking.id
            BASE_URL = f"http://192.168.0.66:5000/bookings/{booking_id}"


            if booking.start_time < now < booking.end_time:
                requests.put(BASE_URL, json={"status": True})
            else:
                requests.put(BASE_URL, json={"status": False})

        time.sleep(60)

update_booking_status()