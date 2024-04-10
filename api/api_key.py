from functools import wraps
from flask import jsonify, request
from config import Config

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
