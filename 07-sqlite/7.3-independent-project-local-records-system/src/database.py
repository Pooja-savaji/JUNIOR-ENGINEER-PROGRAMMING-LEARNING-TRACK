import sqlite3
db = sqlite3.connect("data/records.db")
db.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    course TEXT NOT NULL,
    marks REAL
)
""")

db.commit()
db.close()
print("Database initialized")
