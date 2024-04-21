from utils.db import users, posts, notifications
from uuid import uuid4
from datetime import datetime


"""All helper functions that perform tasks to free up route definitions
"""

def follow(followed, follower):
    try:
        """Follow a user
            - followed: The user to be followed
            - follower: The user that is performing the follow operation
        """
        # Add the follower to the followed follower's list
        users.update_one(
            {'uid': followed},
            {
                '$push': {'followers': follower},
                '$inc': {'follower_count': 1}
            }
        )

        # Add the followed to the follower's following list
        users.update_one(
            {'uid': follower},
            {
                '$push': {'following': followed},
                '$inc': {'following_count': 1}
            }
        )
        return True
    except:
        print('An error occured') # Propper logging to be implemented soon   


def unfollow(unfollowed, unfollower):
    try:
        """Unfollow a user
            - unfollowed: The user to be unfollowed
            - unfollower: The user that is performing the unfollow operation
        """
        # Remove the unfollower from the unfollowed follower's list
        users.update_one(
            {'uid': unfollowed},
            {
                '$pull': {'followers': unfollower},
                '$inc': {'follower_count': -1}
            }
        )

        # Remove the unfollowed from the unfollower's following list
        users.update_one(
            {'uid': unfollower},
            {
                '$pull': {'following': unfollowed},
                '$inc': {'following_count': -1}
            }
        )

        return True
    except:
        print('An error occured') # Propper logging to be implemented soon   


def like_a_post(post_id, user_id):
    try:
        posts.update_one(
            {'pid': post_id},
            {'$push': {'likes': user_id}, '$inc': {'likes_count': 1}}
        )
    except Exception as e:
        print(f'An error occured\n {e}') # Propper logging to be implemented soon


def unlike_a_post(post_id, user_id):
    try:
        posts.update_one(
            {'pid': post_id},
            {'$pull': {'likes': user_id}, '$inc': {'likes_count': -1}}
        )
    except Exception as e:
        print(f'An error occured\n {e}') # Propper logging to be implemented soon  


def create_notification(content, user_id):
    try:
        notifications.insert_one({
            'text': content,
            'nid': str(uuid4()),
            'uid': user_id,
            'read_status': False,
            'create_date': datetime.now()
        })
    except Exception as e:
        print(f'An error occured\n {e}') # Propper logging to be implemented soon