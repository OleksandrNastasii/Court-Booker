from flask import request, jsonify, send_file, Blueprint
from datetime import datetime, timedelta
import threading
import qrcode
from io import BytesIO
import uuid

from app.database.database import db_session
from app.models.user_model import BookingModel, CourtModel, UserModel



booking = Blueprint('booking', __name__)

@booking.route('/bookings', methods=['POST', 'GET'])
def create_booking():
    if request.method == "POST":
        data = request.get_json()
        user_id = data.get("user_id") #this part must be changed to getting from logged in user
        name = data.get("name")
        start_time = datetime.fromisoformat(data.get('start_time'))
        end_time = datetime.fromisoformat(data.get('end_time'))

        # Check availability logic should be here!


        court = CourtModel.query.filter_by(name=name).first()
        if not court:
            return jsonify[{"detail": "Court not found"}], 404

        
        # Generate unique token

        court_id = court.id

        booking = BookingModel.query.filter_by(court_id=court_id).first()
        
        token = uuid.uuid4().hex

        # Save booking
        booking = BookingModel(
            user_id=user_id,
            court_id=court_id,
            start_time=start_time,
            end_time=end_time,
            token=token
        )
        db_session.add(booking)
        db_session.commit()

        def mark_inactive(booking):
            booking.status = False
            db_session.commit()
            return jsonify(f"Court '{court.name}' is now inactive.")

        bookings = BookingModel.query.filter_by(court_id=court.id).all()

        for booking in bookings:
            if booking.status is True:
                if (
                    booking.start_time < start_time < booking.end_time
                    or booking.start_time < end_time < booking.end_time
                ):
                    return jsonify({"detail": "the court is busy at this time"}), 400

        last_booking_end_time = max(booking.end_time for booking in bookings)

        current_time = datetime.now()
        time_to_wait = (last_booking_end_time - current_time).total_seconds()

        if time_to_wait <= 0:
            print(f"The last booking for court '{court.name}' has already ended.")
            booking.status = False
            db_session.commit()
        
        else:
            print(f"Waiting for the booking to end at {last_booking_end_time}...")
            # Set a timer to run the function at the correct time
            threading.Timer(time_to_wait, mark_inactive, [court]).start()



        # Generate QR code pointing to the verification endpoint
        verify_url = f"http://192.168.0.66:5000/verify?token={token}"
        qr = qrcode.make(verify_url)

        img_io = BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')
    if request.method == "GET":
        if request.method == 'GET':
        # Fetch all users
            try:
                bookings = BookingModel.query.all()

                if not bookings:
                    return jsonify({"detail": "No bookings found."}), 200

                return jsonify([booking.show_booking() for booking in bookings]), 200

            except Exception:
                # You can also log the error here for debugging
                return jsonify({"detail": "Internal server error."}), 500
