from models.usermain import UserMain


def authenticate(username, password):
    """
    Given a username and password, select correct user from list
    """
    user = UserMain.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    """
    Extract user_id from payload(content of JWT token)
    """
    user_id = payload['identity']
    return UserMain.find_by_id(user_id)
