from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from datetime import datetime

from app.database.database import db_session
from app.models.user_model import CourtModel, BookingModel

courts_bp = Blueprint("courts", __name__)



@courts_bp.route("/courts", methods=["GET", "POST"])
@login_required
def courts_page():
    
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
    
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        location = data.get("location")
        
        court = CourtModel.query.filter_by(location=location).first()
        
        if court:
            return jsonify({"detail": "Court with this location already exists."}), 409
        
        new_court = CourtModel(
            name=name,
            location=location,
        )

        db_session.add(new_court)
        db_session.commit()

        return jsonify(new_court.show_court()), 201


@courts_bp.route("/courts/<int:court_id>", methods=["GET", "PUT", "DELETE"])
def handle_court(court_id):
    court = CourtModel.query.get(court_id)
    if court is None:
        return jsonify({"detail": "Court not found"}), 404


    if request.method == "GET":
        return jsonify(court.show_court())

    if request.method == "PUT":
        data = request.get_json()
        court.name = data.get("name", court.name)
        court.location = data.get("location", court.location)
        db_session.commit()
        return jsonify({"message": "Court updated"})

    if request.method == "DELETE":
        db_session.delete(court)
        db_session.commit()
        return jsonify({"message": "Court deleted"})
