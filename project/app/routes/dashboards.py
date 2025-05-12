from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from .role_decorators import admin_required, moderator_required

dashboard = Blueprint("dashboard", __name__)

@dashboard.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@dashboard.route('/moderator')
@login_required
@moderator_required
def moderator_dashboard():
    return render_template('moderator_dashboard.html')

@dashboard.route('/user')
@login_required
def user_dashboard():
    return redirect(url_for("courts.html"))