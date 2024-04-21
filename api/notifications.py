from flask import Blueprint, jsonify, session, request
from api.middlewares import api_key_required, login_required
from utils.request_parser import Parser
from utils.db import notifications


"""User notifications
    - Fetch all notifications
    - Fetch all unread notifications
    - Get the count of all unread notifications
    - Update a notifications status to read
"""

notifs = Blueprint('notifs', __name__)


@notifs.route('/api/v1/notifications/view/all', strict_slashes=False)
@api_key_required
@login_required
def fetch_all_notifications():
    current_user = session['user_id']
    all_notifs = list(notifications.find(
        {'uid': current_user}, {'_id': 0}
    ))
    if not all_notifs:
        return jsonify({
            'message': 'no notifications found',
            'status': False
        }), 404
    
    return jsonify({
        'meessage': 'fetched all notifications',
        'status': True,
        'data': all_notifs
    }), 200


@notifs.route('/api/v1/notifications/view/unread', strict_slashes=False)
@api_key_required
@login_required
def fetch_unread_notifications():
    current_user = session['user_id']
    unread_notifs = list(notifications.find(
        {'uid': current_user, 'read_status': False},
        {'_id': 0}
    ))
    if not unread_notifs:
        return jsonify({
            'message': 'no unread notifications found',
            'status': False
        }), 404
    
    return jsonify({
        'meessage': 'fetched all unread notifications',
        'status': True,
        'data': unread_notifs
    }), 200


@notifs.route('/api/v1/notifications/count/unread', strict_slashes=False)
@api_key_required
@login_required
def count_unread_notifications():
    current_user = session['user_id']
    unread_notifs = list(notifications.find(
        {'uid': current_user, 'read_status': False},
        {'_id': 0}
    ))
    
    return jsonify({
        'meessage': 'fetched the number of unread notifications',
        'status': True,
        'data': {
            'notif_count': len(unread_notifs)
        }
    }), 200


@notifs.route('/api/v1/notifications/update/<nid>', methods=['POST'], strict_slashes=False)
@api_key_required
@login_required
def update_notification_status(nid):
    current_user = session['user_id']
    parser = Parser(request.json)
    parser.add_item('read_status', True, help="read_status field can not be blank")
    if not parser.valid:
        return parser.generate_errors(
            'bad request: check the errors field for details on the error',
            400
        )
    
    data = parser.get_items()
    read_status = data['read_status']
    update_status = notifications.update_one(
        {'nid': nid, 'uid': current_user}, {'$set': {'read_status': read_status}}
    )
    if not update_status.matched_count:
        return jsonify({
            'message': 'notification not found for the current user',
            'status': False
        }), 404
    
    return jsonify({
        'message': 'notification status updated',
        'status': True
    }), 200