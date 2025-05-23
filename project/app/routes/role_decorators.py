from flask import abort
from flask_login import current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(401) 
        if not current_user.is_admin():
            return abort(403)  
        return f(*args, **kwargs)
    return decorated_function

def moderator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(401)
        if not current_user.is_moderator() and not current_user.is_admin():
            return abort(403)  
        return f(*args, **kwargs)
    return decorated_function