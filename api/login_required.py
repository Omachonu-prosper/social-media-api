from flask import session, jsonify
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            return jsonify({
                'message': 'unauthorized: you have to be logged in to access this endpoint',
                'status': False
            }), 401
        
        return f(*args, **kwargs)
    return wrapper
