import functools

user = {"username": "jose", "access_level": "guest"}


def make_secure(func):
    @functools.wraps(func) # this is always needed to preserve function original name and docs
    def secure_function(*args, **kwargs):
        if user["access_level"] == "admin":
            return func(*args, **kwargs)
        else:
            return f"No admin permissions for {user['username']}"
    return secure_function

# print(get_admin_password())
# print(secure_get_admin())

@make_secure
def get_admin_password() -> str:
    """Return admin password
    Returns:
        (str): pass str
    """
    return "1234"

@make_secure
def get_password(panel):
    if panel == "admin":
        return "1234"
    elif panel == "billing":
        return "super_secure_password"

print(get_admin_password())
user = {"username": "jose", "access_level": "admin"}
print(get_admin_password())
print(get_password("billing"))