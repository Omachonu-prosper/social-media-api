from flask import Blueprint, jsonify, session, request
from api.middlewares import api_key_required, login_required
from utils.db import notifications


"""User notifications
    - Fetch all notifications
    - Fetch all unread notifications
    - Update a notifications status to read
"""

notifs = Blueprint('notifs', __name__)


@notifs.route('/api/v1/notifications/view/all', strict_slashes=False)
@api_key_required
@login_required
def fetch_all_notifications():
    return "In progress"


@notifs.route('/api/v1/notifications/view/unread', strict_slashes=False)
@api_key_required
@login_required
def fetch_unread_notifications():
    return "In progress"


@notifs.route('/api/v1/notifications/update/<nid>', methods=['POST'], strict_slashes=False)
@api_key_required
@login_required
def fetch_unread_notifications(nid):
    return "In progress"