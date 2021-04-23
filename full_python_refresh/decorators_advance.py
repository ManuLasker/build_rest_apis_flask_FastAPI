import functools

user = {"username": "jose", "access_level": "guest"}
user = {"username": "jose", "access_level": "admin"}



def maske_secure(func):
    @functools.wraps(func) # this is always needed to preserve function original name and docs
    def secure_function():
        if user["access_level"] == "admin":
            return func()
        else:
            return f"No admin permissions for {user['username']}"
    return secure_function

# print(get_admin_password())
# print(secure_get_admin())

@maske_secure
def get_admin_password() -> str:
    """Return admin password
    Returns:
        (str): pass str
    """
    return "1234"

print(get_admin_password.__doc__)