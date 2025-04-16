from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/')
def index():
    return redirect("/signup")

@user_routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)