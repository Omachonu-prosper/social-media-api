from flask import Blueprint, jsonify, request, session
from api.middlewares import api_key_required, login_required
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from uuid import uuid4
from utils.db import users, posts
from utils.helpers import follow, unfollow
from utils.request_parser import Parser

"""All user interactions such as
    - creating posts
    - following other users
    - fetching post feed from the users they follow
    - fetching post feed from other users (fyp)
"""

actions = Blueprint('actions', __name__)

@actions.route('/api/v1/user/post/create', methods=['POST'], strict_slashes=False)
@api_key_required
@login_required
def create_post():
    parser = Parser(request.json)
    parser.add_item('text', True, 'text field can not be empty')
    if not parser.valid:
        return parser.generate_errors(
            'bad request: check the errors field for details on the error',
            400
        )
    
    data = parser.get_items()
    text = data['text']
    user_id = session['user_id']
    post_id = str(uuid4())
    now = datetime.now()
    posts.insert_one({
        'text': text,
        'uid': user_id,
        'created_at': now,
        'pid': post_id
    })

    return jsonify({
        'message': 'post created successfully',
        'status': True
    }), 200


@actions.route('/api/v1/user/follow/<user_id>', methods=['POST'], strict_slashes=False)
@api_key_required
@login_required
def follow_user(user_id):
    executor = ThreadPoolExecutor()
    # Verify the user_id
    if not users.find_one({'uid': user_id}):
        return jsonify({
            'message': 'the user id provided was not found',
            'status': True
        }), 404

    if session['user_id'] == user_id:
        return jsonify({
            'message': 'you can not follow yourself',
            'status': False
        }), 409
    
    executor.submit(follow, user_id, session['user_id'])
    return jsonify({
        'message': 'follow operation successful',
        'status': True
    }), 200


@actions.route('/api/v1/user/unfollow/<user_id>', methods=['POST'], strict_slashes=False)
@api_key_required
@login_required
def unfollow_user(user_id):
    executor = ThreadPoolExecutor()
    # Verify the user_id
    if not users.find_one({'uid': user_id}):
        return jsonify({
            'message': 'the user id provided was not found',
            'status': True
        }), 404

    if session['user_id'] == user_id:
        return jsonify({
            'message': 'you can not unfollow yourself',
            'status': False
        }), 409
    
    executor.submit(unfollow, user_id, session['user_id'])
    return jsonify({
        'message': 'unfollow operation successful',
        'status': True
    }), 200