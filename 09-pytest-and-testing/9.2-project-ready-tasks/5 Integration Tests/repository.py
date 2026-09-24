def save_user(connection, name):
    connection.execute(
        "INSERT INTO users (name) VALUES (?)",
        (name,)
    )
    connection.commit()

def get_user(connection, user_id):
    cursor = connection.execute(
        "SELECT name FROM users WHERE id = ?",
        (user_id,)
    )
    return cursor.fetchone()
