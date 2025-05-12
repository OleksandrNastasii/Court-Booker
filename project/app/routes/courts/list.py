from datetime import datetime

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required

from app.models.user_model import BookingModel, CourtModel, UserModel


courts_list_bp = Blueprint("courts_list", __name__)



@courts_list_bp.route("/courts/list", methods=["GET"])
@login_required
def courts_list_page():
    
    if request.method == "GET":
        start_time_str = request.args.get('start_time')  # Get start time from query params
        end_time_str = request.args.get('end_time')      # Get end time from query params

        courts = CourtModel.query.all()

        if not courts:
            return jsonify({"detail": "No courts found."}), 404

        if not start_time_str or not end_time_str:
            # If no times are selected, return all courts
            return render_template('courts.html', courts=courts)

        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            return jsonify({"detail": "Invalid time format. Use ISO 8601 format."}), 400

        available_courts = []
        for court in courts:
            bookings = BookingModel.query.filter(
                BookingModel.court_id == court.id,
                BookingModel.start_time < end_time,
                BookingModel.end_time > start_time
            ).all()

            if not bookings:
                available_courts.append(court)

        return render_template('courts.html', courts=available_courts)