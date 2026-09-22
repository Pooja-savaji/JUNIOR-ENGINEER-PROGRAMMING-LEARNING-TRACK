import sqlite3
db = sqlite3.connect("data/records.db")
students = db.execute(
    "SELECT * FROM students"
).fetchall()
assert len(students) > 0
print("Test passed")
db.close()
