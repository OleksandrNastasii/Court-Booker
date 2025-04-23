from flask import request, jsonify, send_file, Blueprint
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
import time
import threading
import qrcode
from io import BytesIO
import uuid
from zoneinfo import ZoneInfo

from app.database.database import db_session
from app.models.user_model import BookingModel, CourtModel, UserModel

polish_tz = ZoneInfo("Europe/Warsaw")

booking = Blueprint('booking', __name__)

@booking.route('/bookings', methods=['POST', 'GET'])
def create_booking():
    if request.method == "POST":
        data = request.get_json()

        court_id = data.get("court_id")
        user_id = current_user.id
        start_time = datetime.fromisoformat(data.get("start_time"))
        end_time = datetime.fromisoformat(data.get("end_time"))

        polish_now = datetime.now(ZoneInfo("Europe/Warsaw"))
        polish_now = polish_now.replace(tzinfo=None)

        if start_time < polish_now:
            return jsonify({"error": "Can't book past time"}), 400

        # Check for overlapping bookings
        existing_booking = BookingModel.query.filter(
            BookingModel.court_id == court_id,
            BookingModel.start_time < end_time,
            BookingModel.end_time > start_time
        ).first()

        if existing_booking:
            return jsonify({"error": "Court is already booked at this time."}), 400

        token = uuid.uuid4().hex

        new_booking = BookingModel(
            user_id=user_id,
            court_id=court_id,
            start_time=start_time,
            end_time=end_time,
            token=token,
        )
        db_session.add(new_booking)
        db_session.commit()

        # QR code generation
        verify_url = f"http://192.168.0.66:5000/verify?token={token}"
        qr = qrcode.make(verify_url)
        img_io = BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    if request.method == "GET":
        try:
            bookings = BookingModel.query.all()

            if not bookings:
                return jsonify({"detail": "No bookings found."}), 200

            return jsonify([booking.show_booking() for booking in bookings]), 200

        except Exception:
            # You can also log the error here for debugging
            return jsonify({"detail": "Internal server error."}), 500

@booking.route("/bookings/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    booking = BookingModel.query.get(booking_id)
    if not booking:
        return jsonify({"detail": "Booking not found."}), 404

    try:
        data = request.get_json()
        if not data:
            return jsonify({"detail": "No input data provided."}), 400

        allowed_fields = ["start_time", "end_time", "status", "token", "user_id", "court_id"]

        for key in data:
            if key in allowed_fields:
                setattr(booking, key, data[key])

        db_session.commit()
        return jsonify(booking.show_booking()), 200

    except SQLAlchemyError:
        db_session.rollback()
        return jsonify({"detail": "Database error occurred."}), 500

    except Exception as e:
        return jsonify({"detail": f"Internal server error: {str(e)}"}), 500