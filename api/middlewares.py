from functools import wraps
from flask import jsonify, request, session
from config import Config

"""All app middlewares that get run before the endpoint logic go here
"""


def api_key_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        server_api_key = Config.API_KEY
        client_api_key = request.headers.get('x-api-key', None)
        if not client_api_key:
            return jsonify({
                'message': 'bad request: an API key is required to access this endpoint',
                'status': False
            }), 400
        elif server_api_key != client_api_key:
            return jsonify({
                'message': 'unauthorised: invalid API key',
                'status': False
            }), 401
        
        return f(*args, **kwargs)
    return wrapper 


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({
                'message': 'unauthorized: you have to be logged in to access this endpoint',
                'status': False
            }), 401
        
        return f(*args, **kwargs)
    return wrapper
