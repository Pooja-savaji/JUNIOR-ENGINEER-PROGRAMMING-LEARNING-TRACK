from flask import Flask, request, render_template_string
app = Flask(__name__)

# 1. Hardcoded secret
SECRET_KEY = "my-secret-key"

# Fake user data
users = {
    "pooja": "password123"
}

@app.route("/")
def home():
    return """
    <h1>Simple Login App</h1>
    <form action="/login" method="post">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <button type="submit">Login</button>
    </form>
    """

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # 2. Plaintext password comparison
    if username in users and users[username] == password:
        return f"Welcome {username}!"

    # 3. Information leakage
    return "Invalid username or password. Database login failed."

@app.route("/search")
def search():
    # 4. No input validation
    query = request.args.get("q", "")

    # 5. Possible XSS
    return render_template_string(
        "<h2>Search Result:</h2><p>" + query + "</p>"
    )

@app.route("/admin")
def admin():
    # 6. No authorization check
    return "<h1>Admin Page</h1><p>All users can access this page.</p>"


if __name__ == "__main__":
    app.run(debug=True)
