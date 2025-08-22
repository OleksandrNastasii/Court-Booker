from flask import Blueprint, request, jsonify
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from app.database.database import db_session
from app.models.user_model import CourtModel
from ..role_decorators import admin_required

courts_bp = Blueprint("courts", __name__)


@courts_bp.route("/courts", methods=["GET", "POST"])
@admin_required
def courts_page():
    if request.method == 'GET':
        try:
            courts = CourtModel.query.all()

            if not courts:
                return jsonify({"detail": "No courts found."}), 404

            return jsonify([court.show_court() for court in courts]), 200

        except Exception:
            return jsonify({"detail": "Internal server error."}), 500

    if request.method == "POST":
        try:
            data = request.get_json()

            if not data:
                return jsonify({"detail": "No input data provided."}), 400

            name = data.get("name")
            location = data.get("location")

            if not name or not location:
                return jsonify({"detail": "Both 'name' and 'location' are required."}), 422

            court = CourtModel.query.filter_by(location=location).first()
            if court:
                return jsonify({"detail": "Court with this location already exists."}), 409

            new_court = CourtModel(
                name=name.strip(),
                location=location.strip(),
            )

            db_session.add(new_court)
            db_session.commit()

            return jsonify(new_court.show_court()), 201

        except SQLAlchemyError:
            db_session.rollback()
            return jsonify({"detail": "Database error occurred."}), 500

        except Exception:
            return jsonify({"detail": "Internal server error."}), 500


@courts_bp.route("/courts/<int:court_id>", methods=["GET", "PUT", "DELETE"])
@admin_required
def handle_court(court_id):
    court = CourtModel.query.get(court_id)
    if court is None:
        return jsonify({"detail": "Court not found."}), 404

    if request.method == "GET":
        try:
            return jsonify(court.show_court()), 200
        except Exception:
            return jsonify({"detail": "Internal server error."}), 500

    if request.method == "PUT":
        try:
            data = request.get_json()

            if not data:
                return jsonify({"detail": "No input data provided."}), 400

            location = data.get("location")

            if location:
                existing = CourtModel.query.filter_by(location=location.strip()).first()
                if existing and existing.id != court_id:
                    return jsonify({"detail": "Court with this location already exists."}), 409
                court.location = location.strip()

            db_session.commit()
            return jsonify(court.show_court()), 200

        except SQLAlchemyError:
            db_session.rollback()
            return jsonify({"detail": "Database error occurred."}), 500

        except Exception:
            return jsonify({"detail": "Internal server error."}), 500

    if request.method == "DELETE":
        try:
            db_session.delete(court)
            db_session.commit()
            return jsonify({"detail": "Court deleted successfully."}), 200
        except SQLAlchemyError:
            db_session.rollback()
            return jsonify({"detail": "Database error occurred."}), 500
        except Exception:
            return jsonify({"detail": "Internal server error."}), 500