from werkzeug.security import safe_str_cmp
from src.user import User

users = [
    User(1, 'bob', 'asdf')
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}

# authenticate the user (select the correct user)
def authenticate(username, password):
    user = username_mapping.get(username)
    if user and safe_str_cmp(user.password, password):
        return user
    
# identity function
def identity(payload):
    # payload if the token ot the jwt extension
    user_id = payload['identity']
    return userid_mapping.get(user_id)