from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash
from api.api_key import api_key_required
from utils.db import users
from utils.request_parser import Parser

auth = Blueprint('auth', __name__)

@auth.route('/api/v1/user/signup', methods=['POST'], strict_slashes=False)
@api_key_required
def signup_user():
    parser = Parser(request.json)
    parser.add_item('username', True, 'username filed can not be empty')
    parser.add_item('email', True, 'email field can not be empty')
    parser.add_item('password', True, 'password field can not be empty')
    
    if not parser.valid:
        return parser.generate_errors(
            'bad request: check the errors field for details on the error',
            400
        )
    
    data = parser.items
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password']).decode('utf-8')
    
    if users.find_one({'username': username}):
        return jsonify({
            'message': 'a user with the username already exists',
            'status': False
        }), 409
    
    if users.find_one({'email': email}):
        return jsonify({
            'message': 'a user with the email already exists',
            'status': False
        }), 409
    
    user = users.insert_one({
        'username': username,
        'email': email,
        'password': password
    })

    return jsonify({
        'message': 'user created successfully',
        'status': True
    }), 200