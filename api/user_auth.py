from flask import Blueprint, jsonify

auth = Blueprint('auth', __name__)

@auth.route('/api/v1/user/signup', strict_slashes=False)
def signup_user():
    return jsonify({
        'message': 'user created successfully',
        'status': True
    }), 200