from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
users = {
    "pooja": {
        "password": generate_password_hash("1234"),
        "role": "user"
    },
    "admin": {
        "password": generate_password_hash("admin"),
        "role": "admin"
    }
}
def login(username, password):
    user = users.get(username)

    if user and check_password_hash(user["password"], password):
        return True

    return False

def is_admin(username):
    return users.get(username, {}).get("role") == "admin"
