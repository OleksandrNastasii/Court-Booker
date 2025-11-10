from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

#Blueprint for route to start at app boot
user_routes = Blueprint('user_routes', __name__)

#Redirect to "/signup" endpoint when user visits webpage
@user_routes.route('/')
def index():
    return redirect("/signup")

#Profile page at "/profile endpoint"
@user_routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)