from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..database.database import db_session
from ..models.user_model import UserModel

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        #work on remember option
        remember = True if request.form.get('remember') else False

        user = UserModel.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)

        return redirect(url_for('user_routes.profile'))

    return render_template("login.html")

@auth.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')


        if not email or not name or not password:
            #flash does work, repair it tomorrow
            flash("All fields are required!")
            return redirect(url_for('auth.signup'))

        user = UserModel.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.login'))

        new_user = UserModel(
            email=email, 
            name=name, 
            password=generate_password_hash(password,
                                             method='pbkdf2:sha256')
                                            )

        db_session.add(new_user)
        db_session.commit()

        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    return redirect("/login")