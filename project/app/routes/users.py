from flask import Blueprint, request, jsonify
from flask_login import login_required
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from app.database.database import db_session
from app.models.user_model import UserModel
from app.schemas.user_schemas import UserCreateSchema
from .role_decorators import admin_required

#Marshmallow schema for validation
user_schema = UserCreateSchema()

#Blueprint for routes to start at boot
user = Blueprint('user', __name__)

#Logic for POST and GET at "/users" endpoint that requires admin to be accessed
@user.route('/users', methods=['GET', 'POST'])
@admin_required
def get_post():

    #Checks whether HTTP method is GET
    if request.method == 'GET':

        #If method is GET starts this try except logic
        try:

            #REtrieves all users data from database
            users = UserModel.query.all()

            #If there is no user returns "No users found"
            if not users:
                return jsonify({"detail": "No users found."}), 200

            #Returns all users if there are any 
            return jsonify([user.show_user() for user in users]), 200

        #exception for Internal server error
        except Exception:
            return jsonify({"detail": "Internal server error."}), 500
            
    #Checks whether HTTP method is POST
    if request.method == 'POST':

        #Try except block for POST
        try:

            #Retrieves data from user's request
            data = request.get_json()

            #Validates data with user schema
            validated_data = user_schema.load(data)

            #Retrieves user's data after validation
            name = validated_data['name'].strip()
            email = validated_data['email'].strip()
            password = validated_data['password']
            role = validated_data["role"]

            #Checks whether user with this email already exists
            existing_user = UserModel.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({"detail": "User with this email already exists."}), 409

            #Creates new user in the database
            new_user = UserModel(email=email,
                                name=name,
                                role=role,
                                password=generate_password_hash(password, method='pbkdf2:sha256'))
            
            #Adds user to database and commits changes in the database
            db_session.add(new_user)
            db_session.commit()

            #Returns user data after creation
            return jsonify(new_user.show_user()), 201
            
        #REsponse for data that did not pass validation
        except ValidationError as err:
            return jsonify({"detail": err.messages}), 422

        #Response if there is an issue with database
        except SQLAlchemyError:
            db_session.rollback()
            return jsonify({"detail": "Database error occurred."}), 500

        #Response if there is anInternal server error
        except Exception as e:
            return jsonify({"detail": "Internal server error."}), 500

#Logic for PUT, GET and DELETE which require user id, runs at "/users/id" endpoint
@user.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def get_put_delete(user_id):

    #Gets user by id
    user = UserModel.query.get(user_id)

    #Response if there is no user with this id
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    #Checks whether method is GET
    if request.method == 'GET':

        #Returns user data
        try:
            return jsonify(user.show_user()), 200
        
        #Returns Internal server error as exception
        except Exception:
            return jsonify({"detail": "Internal server error"}), 500

    #Checks whether method is PUT
    elif request.method == 'PUT':


        try:

            #Takes input data from request
            data = request.get_json()

            #Responsfor no provided data
            if not data:
                return jsonify({"detail": "No input data provided."}), 400

            #Validates data
            validated_data = user_schema.load(data, partial=True)

            #Retireves email for validated data
            new_email = validated_data.get("email")

            #Checks whether new email and email of user are not the same
            if new_email and new_email != user.email:

                #Checks whether user with this email exists
                existing_user = UserModel.query.filter_by(email=new_email).first()
                
                #Response if user with this email already exists
                if existing_user:
                    return jsonify({"detail": "User with this email already exists."}), 409

            #Validation for password
            if "password" in validated_data:
                validated_data["password"] = generate_password_hash(
                    validated_data["password"], method='pbkdf2:sha256'
                )

            #Assigns all changed values
            for key, value in validated_data.items():
                setattr(user, key, value)

            #Commits changes in database
            db_session.commit()

            #Returns user data
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