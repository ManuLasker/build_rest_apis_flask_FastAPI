from werkzeug.security import check_password_hash
from src.models import UserModel

# authenticate the user (select the correct user)
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and check_password_hash(user.password, password):
        return user
    
# identity function
def identity(payload):
    # payload if the token ot the jwt extension
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)