from flask import abort
from flask_login import current_user
from functools import wraps

#Decorator for checking whether user is admin 
def admin_required(f):

    #Wrapper to save metadata of decorated function
    @wraps(f)

    #Defined decorated function
    def decorated_function(*args, **kwargs):

        #Checks whether user is authenticated, if not returns 401 HTTP response
        if not current_user.is_authenticated:
            return abort(401) 
        
        #Checks whether user is admin, if not returns 403 HTTP response
        if not current_user.is_admin():
            return abort(403)  
        
        #Returns wrapped function with all arguments, works if all checks were passed
        return f(*args, **kwargs)
    
    #Returns function without arguments if checks were not passed
    return decorated_function


#Decorator for checking whether user is admin 
def moderator_required(f):

    #Wrapper to save metadata of decorated function
    @wraps(f)

    #Defined decorated function
    def decorated_function(*args, **kwargs):

        #Checks whether user is authenticated, if not returns 401 HTTP response
        if not current_user.is_authenticated:
            return abort(401)
        
        #Checks whether user is moderator, if not returns 403 HTTP response
        if not current_user.is_moderator() and not current_user.is_admin():
            return abort(403)  
        
        #Returns wrapped function with all arguments, works if all checks were passed
        return f(*args, **kwargs)
    
    #Returns function without arguments if checks were not passed
    return decorated_function