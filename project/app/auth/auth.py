from flask import Blueprint, render_template, redirect, request, jsonify, flash, url_for
from flask_login import login_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
import traceback

from ..database.database import db_session
from ..models.user_model import UserModel
from app.schemas.user_schemas import UserCreateSchema, UserLoginSchema

user_create_schema = UserCreateSchema()
user_login_schema = UserLoginSchema()

auth = Blueprint('auth', __name__)

from flask import jsonify

@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        try:
            data = request.get_json()

            # Validate using schema
            validated_data = user_login_schema.load(data)

            email = validated_data['email']
            password = validated_data['password']

            user = UserModel.query.filter_by(email=email).first()

            if not user or not check_password_hash(user.password, password):
                return jsonify({"message": "Invalid email or password"}), 401

            login_user(user)
            
            if user.role == 'admin':
                redirect_url = url_for("dashboard.admin_dashboard")
            elif user.role == 'moderator':
                redirect_url = url_for("dashboard.moderator_dashboard")
            else:
                redirect_url = url_for('courts_list.courts_list_page')

            return jsonify({"message": "Login successful", "redirect": redirect_url}), 200

        except ValidationError as err:
            return jsonify({"detail": err.messages}), 400
        
        except Exception:
            traceback.print_exc()  # This logs the actual error to your console
            return jsonify({"message": "Internal server error"}), 500

    return render_template("login.html")




@auth.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        try:
            data = request.get_json()

            # Validate input using schema
            validated_data = user_create_schema.load(data)

            name = validated_data['name'].strip()
            email = validated_data['email'].strip()
            password = validated_data['password']

            # Check if user already exists
            existing_user = UserModel.query.filter_by(email=email).first()
            if existing_user:
                flash("User with this email already exists")
                return jsonify({"detail": "User with this email already exists."}), 409

            # Create new user with hashed password
            new_user = UserModel(
                email=email,
                name=name,
                password=generate_password_hash(password, method='pbkdf2:sha256')
            )

            db_session.add(new_user)
            db_session.commit()

            return jsonify({"message": "User created successfully!"}), 201

        except ValidationError as err:
            return jsonify({"detail": err.messages}), 422

        except SQLAlchemyError:
            db_session.rollback()
            return jsonify({"detail": "Database error occurred."}), 500

        except Exception:
            return jsonify({"detail": "Internal server error."}), 500

    # For GET requests, render the signup page
    return render_template('signup.html')


@auth.route('/logout')
def logout():
    return redirect("/login")