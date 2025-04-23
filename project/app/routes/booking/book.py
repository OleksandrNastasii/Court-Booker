from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required

from app.models.user_model import BookingModel, CourtModel, UserModel


book = Blueprint("booking_page", __name__)

@book.route('/booking', methods=['GET'])
@login_required
def booking_page():
    court_id = request.args.get('court_id')
    court = CourtModel.query.filter_by(id=court_id).first()
    
    if not court:
        return jsonify({"detail": "Court not found"}), 404

    return render_template("booking.html", court=court)
