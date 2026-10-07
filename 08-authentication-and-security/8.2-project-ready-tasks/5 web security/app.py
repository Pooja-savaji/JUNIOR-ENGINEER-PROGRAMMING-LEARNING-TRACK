from flask import Flask, request
app = Flask(__name__)

users = {
    "pooja": "user",
    "admin": "admin"
}

@app.route("/admin")
def admin():
    username = request.args.get("user")

    if users.get(username) != "admin":
        return "Access Denied"

    return "Welcome Admin"

@app.route("/search")
def search():
    name = request.args.get("name", "")
    return f"Hello, {name}"

if __name__ == "__main__":
    app.run()
