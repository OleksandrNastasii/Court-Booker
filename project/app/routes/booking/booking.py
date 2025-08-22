from flask import request, jsonify, send_file, Blueprint, make_response
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import qrcode
from io import BytesIO
import uuid
from zoneinfo import ZoneInfo

from app.database.database import db_session
from app.models.user_model import BookingModel
from ..role_decorators import admin_required

polish_tz = ZoneInfo("Europe/Warsaw")

booking = Blueprint('booking', __name__)


@booking.route('/bookings', methods=['POST'])
@login_required
def create_booking():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"detail": "No input data provided."}), 400

        court_id = data.get("court_id")
        start_time_str = data.get("start_time")
        end_time_str = data.get("end_time")

        if not court_id or not start_time_str or not end_time_str:
            return jsonify({"detail": "Missing required fields: 'court_id', 'start_time', or 'end_time'."}), 422

        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            return jsonify({"detail": "Invalid datetime format. Use ISO 8601."}), 422

        if start_time >= end_time:
            return jsonify({"detail": "Start time must be before end time."}), 422

        now = datetime.now(polish_tz).replace(tzinfo=None)
        if start_time < now:
            return jsonify({"detail": "Cannot book time in the past."}), 400

        overlap = BookingModel.query.filter(
            BookingModel.court_id == court_id,
            BookingModel.start_time < end_time,
            BookingModel.end_time > start_time
        ).first()

        if overlap:
            return jsonify({"detail": "Court is already booked at this time."}), 400

        token = uuid.uuid4().hex
        user_id = current_user.id

        new_booking = BookingModel(
            user_id=user_id,
            court_id=court_id,
            start_time=start_time,
            end_time=end_time,
            token=token
        )

        db_session.add(new_booking)
        db_session.commit()

        verify_url = f"http://192.168.0.66:5000/verify?token={token}"
        qr = qrcode.make(verify_url)
        img_io = BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)

        response = make_response(send_file(img_io, mimetype='image/png'))
        response.headers["X-Booking-ID"] = str(new_booking.id)

        return response

    except SQLAlchemyError:
        db_session.rollback()
        return jsonify({"detail": "Database error occurred."}), 500

    except Exception:
        return jsonify({"detail": "Internal server error."}), 500


@booking.route('/bookings', methods=['GET'])
@admin_required
def get_bookings():
    try:
        bookings = BookingModel.query.all()

        if not bookings:
            return jsonify({"detail": "No bookings found."}), 404

        return jsonify([b.show_booking() for b in bookings]), 200

    except Exception:
        return jsonify({"detail": "Internal server error."}), 500


@booking.route("/bookings/<int:booking_id>", methods=["PUT"])
@admin_required
def update_booking(booking_id):
    booking = BookingModel.query.get(booking_id)
    if not booking:
        return jsonify({"detail": "Booking not found."}), 404

    try:
        data = request.get_json()
        if not data:
            return jsonify({"detail": "No input data provided."}), 400

        allowed_fields = ["start_time", "end_time", "status", "token", "user_id", "court_id"]

        for key in allowed_fields:
            if key in data:
                setattr(booking, key, data[key])

        db_session.commit()
        return jsonify(booking.show_booking()), 200

    except SQLAlchemyError:
        db_session.rollback()
        return jsonify({"detail": "Database error occurred."}), 500

    except Exception:
        return jsonify({"detail": "Internal server error."}), 500

@booking.route("/bookings/<int:booking_id>", methods=["GET"])
@admin_required
def get_booking_by_id(booking_id):
    try:
        booking = BookingModel.query.get(booking_id)
        if not booking:
            return jsonify({"detail": "Booking not found."}), 404
        return jsonify(booking.show_booking()), 200
    except Exception:
        return jsonify({"detail": "Internal server error."}), 500


@booking.route("/bookings/<int:booking_id>", methods=["DELETE"])
@admin_required
def delete_booking(booking_id):
    booking = BookingModel.query.get(booking_id)
    if not booking:
        return jsonify({"detail": "Booking not found."}), 404

    try:
        db_session.delete(booking)
        db_session.commit()
        return jsonify({"detail": "Booking deleted successfully."}), 200
    except SQLAlchemyError:
        db_session.rollback()
        return jsonify({"detail": "Database error occurred."}), 500
    except Exception:
        return jsonify({"detail": "Internal server error."}), 500

