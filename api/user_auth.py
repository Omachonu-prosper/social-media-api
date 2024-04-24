from flask import Blueprint, jsonify, request, session
from uuid import uuid4
from flask_bcrypt import generate_password_hash, check_password_hash
from api.middlewares import api_key_required
from utils.db import users
from utils.request_parser import Parser

auth = Blueprint('auth', __name__)

@auth.route('/api/v1/auth/signup', methods=['POST'], strict_slashes=False)
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
    user_id = str(uuid4())
    
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
    
    users.insert_one({
        'uid': user_id,
        'username': username,
        'email': email,
        'password': password
    })

    session['user_id'] = user_id
    return jsonify({
        'message': 'user created successfully',
        'status': True
    }), 201


@auth.route('/api/v1/auth/login', methods=['POST'], strict_slashes=False)
@api_key_required
def login():
    parser = Parser(request.json)
    parser.add_item('email', True, 'email field can not be empty')
    parser.add_item('password', True, 'password field can not be empty')
    
    if not parser.valid:
        return parser.generate_errors(
            'bad request: check the errors field for details on the error',
            400
        )
    
    data = parser.get_items()
    email = data['email']
    password = data['password']
    user = users.find_one({'email': email}, {'_id': 0})
    
    if not user:
        return jsonify({
            'message': 'no user was found with the provided email address',
            'status': False
        }), 404
    
    if not check_password_hash(user['password'], password):
        # Passwords do not match
        return jsonify({
            'message': 'unauthorized: incorrect password',
            'status': False
        }), 401
    
    session['user_id'] = user['uid']
    return jsonify({
        'message': 'user login successful',
        'status': True
    }), 200


@auth.route('/api/v1/auth/logout', methods=['POST'], strict_slashes=False)
@api_key_required
def logout():
    session.clear()

    return jsonify({
        'message': 'user logout successful',
        'status': True
    }), 200