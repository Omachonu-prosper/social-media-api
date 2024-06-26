from flask import Blueprint, jsonify, request, session
from api.middlewares import api_key_required, login_required
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from uuid import uuid4
from utils.db import users, posts
from utils.helpers import follow, unfollow, like_a_post, unlike_a_post, create_notification
from utils.request_parser import Parser


"""All user interactions such as
    - creating posts
    - following other users
    - fetching post feed from the users they follow
    - fetching post feed from other users (fyp)
    - liking a post
    - commenting on a post
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
    }), 201


@actions.route('/api/v1/user/follow/<user_id>', methods=['POST'], strict_slashes=False)
@api_key_required
@login_required
def follow_user(user_id):
    executor = ThreadPoolExecutor()
    current_user = session['user_id']

    # Verify the user_id
    if not users.find_one({'uid': user_id}):
        return jsonify({
            'message': 'the user id provided was not found',
            'status': False
        }), 404

    if current_user == user_id:
        return jsonify({
            'message': 'you can not follow yourself',
            'status': False
        }), 403
    
    # If you follow the user already
    if users.find_one({'uid': current_user, 'following': user_id}):
        return jsonify({
            'message': 'you already follow this user',
            'status': False
        }), 409
    
    executor.submit(follow, user_id, current_user)
    notification_content = "You have a new follower"
    executor.submit(create_notification, notification_content, user_id)
    return jsonify({
        'message': 'follow operation successful',
        'status': True
    }), 200


@actions.route('/api/v1/user/unfollow/<user_id>', methods=['POST'], strict_slashes=False)
@api_key_required
@login_required
def unfollow_user(user_id):
    executor = ThreadPoolExecutor()
    current_user = session['user_id']

    # Verify the user_id
    if not users.find_one({'uid': user_id}):
        return jsonify({
            'message': 'the user id provided was not found',
            'status': False
        }), 404

    if current_user == user_id:
        return jsonify({
            'message': 'you can not unfollow yourself',
            'status': False
        }), 403
    
    # If you do not follow the user already
    if not users.find_one({'uid': current_user, 'following': user_id}):
        return jsonify({
            'message': 'you do not follow this user',
            'status': False
        }), 409
    
    executor.submit(unfollow, user_id, current_user)
    return jsonify({
        'message': 'unfollow operation successful',
        'status': True
    }), 200


@actions.route('/api/v1/user/feed/following', strict_slashes=False)
@api_key_required
@login_required
def view_following_feed():
    # Fetch all the users that the current user follows
    current_user_id = session['user_id']
    following = list(users.find(
        {'uid': current_user_id},
        {'following': 1, '_id': 0}
    ))[0].get('following')
    if not following:
        # The current user doesnt follow anyone
        return jsonify({
            'message': 'no posts in your following because you do not currently follow anyone',
            'status': False
        }), 404

    following_posts = list(posts.find(
        {'uid': {'$in': following}},
        {'_id': 0}
    ).sort({'created_at': 1}))
    if not following_posts:
        return jsonify({
            'message': 'no posts could be fetched at the moment',
            'status': False
        }), 404
    
    return jsonify({
        'message': 'fetched your news feed successfully',
        'data': following_posts,
        'status': True
    }), 200


@actions.route('/api/v1/user/feed/fyp', strict_slashes=False)
@api_key_required
@login_required
def view_fyp_feed():
    # Fetch all posts except those of the current user and sort by date
    current_user_id = session['user_id']
    fyp_posts = list(posts.find(
        {'uid': {'$ne': current_user_id}},
        {'_id': 0}
    ).sort({'created_at': 1}))
    if not fyp_posts:
        return jsonify({
            'message': 'no posts could be fetched at the moment',
            'status': False
        }), 404
    
    return jsonify({
        'message': 'fetched your news feed successfully',
        'data': fyp_posts,
        'status': True
    }), 200
    

@actions.route('/api/v1/posts/<post_id>/like', methods=['POST'], strict_slashes=False)
@api_key_required
@login_required
def like_post(post_id):
    executor = ThreadPoolExecutor()
    user_id = session['user_id']
    post = posts.find_one({'pid': post_id})
    if not post:
        return jsonify({
            'message': 'the post id does not match any post in the database',
            'status': False
        }), 404
    
    if posts.find_one({'pid': post_id, 'likes': user_id}):
        return jsonify({
            'message': 'you can not like a post more than once',
            'status': False
        }), 403
    
    executor.submit(like_a_post, post_id, user_id)
    
    post_owner = post['uid']
    post_text = post['text'][0:20]
    notification_content = f'Your post "{post_text}..." has a new like'
    executor.submit(create_notification, notification_content, post_owner)
    
    return jsonify({
        'message': 'like operation successful',
        'status': True
    }), 200


@actions.route('/api/v1/posts/<post_id>/unlike', methods=['POST'], strict_slashes=False)
@api_key_required
@login_required
def unlike_post(post_id):
    user_id = session['user_id']
    post = posts.find_one({'pid': post_id})
    if not post:
        return jsonify({
            'message': 'the post id does not match any post in the database',
            'status': False
        }), 404
    
    if not posts.find_one({'pid': post_id, 'likes': user_id}):
        return jsonify({
            'message': 'you can not unlike a post that you have not previously liked',
            'status': False
        }), 403
    
    unlike_a_post(post_id, user_id)
    return jsonify({
        'message': 'unlike operation successful',
        'status': True
    }), 200


@actions.route('/api/v1/post/<post_id>/comment/new', methods=['POST'], strict_slashes=False)
@api_key_required
@login_required
def new_comment(post_id):
    executor = ThreadPoolExecutor()
    parser = Parser(request.json)
    current_user = session['user_id']
    parser.add_item('text', True, 'text field can not be left blank')
    if not parser.valid:
        return parser.generate_errors(
            'bad request: check the errors field for details on the error',
            400
        )
    
    data = parser.get_items()
    text = data['text']
    post = posts.find_one_and_update(
        {'pid': post_id},
        {
            '$push': {'comments': {
                'text': text, 'uid': current_user
            }},
            '$inc': {'comments_count': 1}
        }
    )
    if not post:
        return jsonify({
            'message': 'post id not found',
            'status': False
        }), 404

    notif_user_id = post['uid']
    comment_content = text[0:20]
    notif_content = f'Your post has a new coment "{comment_content}..."'
    executor.submit(create_notification, notif_content, notif_user_id)
    
    return jsonify({
        'message': 'comment created successfully',
        'status': True
    }), 201