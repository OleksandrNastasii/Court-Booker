from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from .role_decorators import admin_required, moderator_required

#Creates Blueprint for dashboards to start at website boot
dashboard = Blueprint("dashboard", __name__)

#Creates "/admin" endpoint using admin_dashboard.html and sets resritction with access rights
@dashboard.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

#Creates "/moderator" endpoint using moderator_dashboard.html and sets resritction with access rights
@dashboard.route('/moderator')
@login_required
@moderator_required
def moderator_dashboard():
    return render_template('moderator_dashboard.html')

#Redirects user to court selection page
@dashboard.route('/user')
@login_required
def user_dashboard():
    return redirect(url_for("courts.html"))