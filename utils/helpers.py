from utils.db import users, posts

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
            {'$push': {
                "followers": follower
            }}
        )

        # Add the followed to the follower's following list
        users.update_one(
            {'uid': follower},
            {'$push': {
                "following": followed
            }}
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
            {'$pull': {
                "followers": unfollower
            }}
        )

        # Remove the unfollowed from the unfollower's following list
        users.update_one(
            {'uid': unfollower},
            {'$pull': {
                "following": unfollowed
            }}
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