import sqlite3
db = sqlite3.connect("data/records.db")

db.execute(
    "INSERT INTO students (name, course, marks) VALUES (?, ?, ?)",
    ("Pooja", "CSE", 85)
)

print("Students:")
print(db.execute("SELECT * FROM students").fetchall())

print("Search:")
print(db.execute(
    "SELECT * FROM students WHERE name = ?", ("Pooja",)
).fetchall())

print("Filter:")
print(db.execute(
    "SELECT * FROM students WHERE marks >= ?", (80,)
).fetchall())

print("Report:")
print(db.execute(
    "SELECT COUNT(*), AVG(marks) FROM students"
).fetchone())

db.commit()
db.close()
