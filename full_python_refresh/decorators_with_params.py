import functools

user = {"username": "jose", "access_level": "guest"}


def make_secure(access_level):
    def decorator(func):
        @functools.wraps(func) # this is always needed to preserve function original name and docs
        def secure_function(*args, **kwargs):
            if user["access_level"] == access_level:
                return func(*args, **kwargs)
            else:
                return f"No {access_level} permissions for {user['username']}"
        return secure_function
    return decorator

@make_secure("admin")
def get_admin_password() -> str:
    """Return admin password
    Returns:
        (str): pass str
    """
    return "admin: 1234"

@make_secure("user")
def get_dashboard_password() -> str:
    return "user: user_password"

@make_secure("admin")
def get_password(panel):
    if panel == "admin":
        return "1234"
    elif panel == "billing":
        return "super_secure_password"

# user = {"username": "jose", "access_level": "admin"}
# print(get_admin_password())
# # user = {"username": "jose", "access_level": "admin"}
# # print(get_admin_password())
# user = {"username": "jose", "access_level": "admin"}
# print(get_dashboard_password())