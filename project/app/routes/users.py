from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from app.database.database import db_session
from app.models.user_model import UserModel
from app.schemas.user_schemas import UserCreateSchema

user_schema = UserCreateSchema()

user = Blueprint('user', __name__)

@user.route('/users', methods=['GET', 'POST'])
def get_post():
    if request.method == 'GET':
        # Fetch all users
        try:
            users = UserModel.query.all()

            if not users:
                return jsonify({"detail": "No users found."}), 200

            return jsonify([user.show_user() for user in users]), 200

        except Exception:
            # You can also log the error here for debugging
            return jsonify({"detail": "Internal server error."}), 500
        
    elif request.method == 'POST':
        try:
            data = request.get_json()

            validated_data = user_schema.load(data)

            name = validated_data['name'].strip()
            email = validated_data['email'].strip()
            password = validated_data['password']

            # Check if user with this email already exists
            existing_user = UserModel.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({"detail": "User with this email already exists."}), 409

            # Create and save new user
            new_user = UserModel(email=email,
                                name=name,
                                password=generate_password_hash(password, method='pbkdf2:sha256'))
            db_session.add(new_user)
            db_session.commit()

            return jsonify(new_user.show_user()), 201
        
        except ValidationError as err:
            return jsonify({"detail": err.messages}), 422

        except SQLAlchemyError:
            db_session.rollback()
            return jsonify({"detail": "Database error occurred."}), 500

        except Exception as e:
            # Log the actual error in real apps
            return jsonify({"detail": "Internal server error."}), 500

@user.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_put_delete(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    if request.method == 'GET':
        try:
            return jsonify(user.show_user()), 200
        except Exception:
            return jsonify({"detail": "Internal server error"}), 500

    elif request.method == 'PUT':
        # Update user details
        try:
            data = request.get_json()
            if not data:
                return jsonify({"detail": "No input data provided."}), 400

            validated_data = user_schema.load(data, partial=True)

            new_email = validated_data.get("email")
            if new_email and new_email != user.email:
                existing_user = UserModel.query.filter_by(email=new_email).first()
                if existing_user:
                    return jsonify({"detail": "User with this email already exists."}), 409

            if "password" in validated_data:
                validated_data["password"] = generate_password_hash(
                    validated_data["password"], method='pbkdf2:sha256'
                )

            for key, value in validated_data.items():
                setattr(user, key, value)

            db_session.commit()
            return jsonify(user.show_user()), 200

        except ValidationError as err:
            return jsonify({"detail": err.messages}), 422

        except SQLAlchemyError:
            db_session.rollback()
            return jsonify({"detail": "Database error occurred."}), 500

        except Exception:
            return jsonify({"detail": "Internal server error."}), 500
    
    elif request.method == 'DELETE':
        try:
            db_session.delete(user)
            db_session.commit()
            return jsonify({"detail": "User deleted successfully."}), 200
        except Exception:
            db_session.rollback()
            return jsonify({"detail": "Internal server error."}), 500