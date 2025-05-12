from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.database.database import db_session
from app.models.user_model import CourtModel
from ..role_decorators import admin_required

courts_bp = Blueprint("courts", __name__)



@courts_bp.route("/courts", methods=["GET", "POST"])
@admin_required
def courts_page():
    
    if request.method == 'GET':
        # Fetch all users
        try:
            courts = CourtModel.query.all()

            if not courts:
                return jsonify({"detail": "No users found."}), 200

            return jsonify([court.show_court() for court in courts]), 200

        except Exception:
            # You can also log the error here for debugging
            return jsonify({"detail": "Internal server error."}), 500
        
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
@admin_required
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
