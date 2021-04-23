user = {"username": "jose", "access_level": "guest"}
# user = {"username": "jose", "access_level": "admin"}


def get_admin_password():
    return "1234"

def secure_get_admin():
    if user["access_level"] == "admin":
        return "1234"

def maske_secure(func):
    def secure_function():
        if user["access_level"] == "admin":
            return func()
        else:
            return f"No admin permissions for {user['username']}"
    return secure_function

# print(get_admin_password())
# print(secure_get_admin())

get_admin_password = maske_secure(get_admin_password)
print(get_admin_password())