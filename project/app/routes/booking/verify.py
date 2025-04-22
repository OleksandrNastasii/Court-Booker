from datetime import datetime
from flask import Blueprint, request, jsonify
from app.models.user_model import BookingModel


verify = Blueprint("verify", __name__)

@verify.route('/verify', methods=['GET'])
def verify_token():
    token = request.args.get('token')
    booking = BookingModel.query.filter_by(token=token).first()

    if not booking:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 400

    now = datetime.now()
    if booking.start_time <= now <= booking.end_time:
        return jsonify({'status': 'success', 'message': 'Access granted'})
    else:
        return jsonify({'status': 'error', 'message': 'Access denied - wrong time',
                        "time": f"{booking.start_time}, {now},{booking.end_time}"})
