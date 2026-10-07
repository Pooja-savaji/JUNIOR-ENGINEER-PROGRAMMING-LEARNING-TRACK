from werkzeug.security import generate_password_hash, check_password_hash

users = {}

# Register user
username = "pooja"
password = "123456"

users[username] = generate_password_hash(password)

print("Password hash:", users[username])

# Login
login_password = "123456"

if check_password_hash(users[username], login_password):
    print("Login successful")
else:
    print("Wrong password")
