import sqlite3

def create_database():
    connection = sqlite3.connect(":memory:")

    connection.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)

    return connection
