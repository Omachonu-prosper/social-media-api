from flask import Blueprint, jsonify
from api.api_key import api_key_required
from utils.db import users

auth = Blueprint('auth', __name__)

@auth.route('/api/v1/user/signup', strict_slashes=False)
@api_key_required
def signup_user():    
    return jsonify({
        'message': 'user created successfully',
        'status': True
    }), 200