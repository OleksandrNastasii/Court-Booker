from flask import Blueprint, render_template, redirect, request, jsonify, flash, url_for
from flask_login import login_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
import traceback

from ..database.database import db_session
from ..models.user_model import UserModel
from app.schemas.user_schemas import UserCreateSchema, UserLoginSchema

#Defined User Schema
user_create_schema = UserCreateSchema()

#Defined Login Schema
user_login_schema = UserLoginSchema()

#Defined blueprint for authentification 
auth = Blueprint('auth', __name__)

#Created webpage "/login"
@auth.route("/login", methods=["POST", "GET"])
def login():

    #Checks whether it is POST method for /login
    if request.method == "POST":

        #Try except block for POST method
        try:

            #Retrieves data from user's request
            data = request.get_json()

            #Validates data from user's request
            validated_data = user_login_schema.load(data)

            #Retrieves email from user's request
            email = validated_data['email']

            #Retrieves password from user's request 
            password = validated_data['password']

            #Retrieves data of user from database using email as identifier 
            user = UserModel.query.filter_by(email=email).first()

            #Checks whether user with this email and password exists in the database
            if not user or not check_password_hash(user.password, password):
                return jsonify({"message": "Invalid email or password"}), 401

            #Starts login session for user
            login_user(user)
            
            #Checks what role user has in the database(admin, moderator, user)
            if user.role == 'admin':
                redirect_url = url_for("dashboard.admin_dashboard")
            elif user.role == 'moderator':
                redirect_url = url_for("dashboard.moderator_dashboard")
            else:
                redirect_url = url_for('courts_list.courts_list_page')

            #Returns user's data if successful
            return jsonify({"message": "Login successful", "redirect": redirect_url, "id": f"{user.id}"}), 200

        #Returns Bad Request errors
        except ValidationError as err:
            return jsonify({"detail": err.messages}), 400
        
        #Returns Internal Server error
        except Exception:
            traceback.print_exc()
            return jsonify({"message": "Internal server error"}), 500

    #Returns page's layout and renders the page if GET request was made
    return render_template("login.html")

#Created webpage "/signup"
@auth.route('/signup', methods=["POST", "GET"])
def signup():

    #Checks whether it is POST method for /signup
    if request.method == "POST":

        #Try Except block for POST method on /signup page
        try:

            #Retrieves data from user's request
            data = request.get_json()

            #Validates data from, user's request 
            validated_data = user_create_schema.load(data)

            #Retrieves name from user's data
            name = validated_data['name'].strip()

            #Retrieves email from user's data
            email = validated_data['email'].strip()

            #Retrieves password from user's data
            password = validated_data['password']

            #Looks for the user with the same email in the database
            existing_user = UserModel.query.filter_by(email=email).first()

            #Checks whether user with that email exists
            if existing_user:
                flash("User with this email already exists")
                return jsonify({"detail": "User with this email already exists."}), 409

            #Creates a new user using UserModel
            new_user = UserModel(
                email=email,
                name=name,
                password=generate_password_hash(password, method='pbkdf2:sha256')
            )

            #Adds and commits new user to the database
            db_session.add(new_user)
            db_session.commit()

            #Returns if user was created successfully
            return jsonify({"message": "User created successfully!"}), 201

        #returns 422 for any validation error
        except ValidationError as err:
            return jsonify({"detail": err.messages}), 422

        #returns 500 for any database error
        except SQLAlchemyError:
            db_session.rollback()
            return jsonify({"detail": "Database error occurred."}), 500

        #returns 500 for any internal server error
        except Exception:
            return jsonify({"detail": "Internal server error."}), 500

    #Renders page if request method was GET
    return render_template('signup.html')

#REdirects to /login if visiting /logout page
@auth.route('/logout')
def logout():
    return redirect("/login")