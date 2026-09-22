import sqlite3
db = sqlite3.connect("inventory.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL
)
""")

cur.execute(
    "INSERT INTO products (name, price) VALUES (?, ?)",
    ("Mouse", 500)
)

cur.execute("SELECT * FROM products")
print(cur.fetchall())

cur.execute(
    "UPDATE products SET price = ? WHERE id = ?",
    (600, 1)
)

cur.execute(
    "DELETE FROM products WHERE id = ?",
    (1,)
)

db.commit()
db.close()
