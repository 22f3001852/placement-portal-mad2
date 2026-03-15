from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from functools import wraps

def role_required(required_role):
    def decorator(func):
        @wraps(func) # it allows us to use a same token for various endpoints without having to repeat the jwt_required decorator
        @jwt_required() # ensures that the user is authenticated 
        def wrapper(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify("Unauthorized"), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


