from werkzeug.security import safe_str_cmp, check_password_hash
from src.user import User

# authenticate the user (select the correct user)
def authenticate(username, password):
    user = User.find_by_username(username)
    if user and check_password_hash(user.password, password):
        return user
    
# identity function
def identity(payload):
    # payload if the token ot the jwt extension
    user_id = payload['identity']
    return User.find_by_id(user_id)