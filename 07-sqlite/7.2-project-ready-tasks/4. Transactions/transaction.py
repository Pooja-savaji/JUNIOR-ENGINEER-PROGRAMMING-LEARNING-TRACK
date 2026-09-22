import sqlite3
db = sqlite3.connect("bank.db")
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, balance REAL)")
cur.execute("DELETE FROM accounts")
cur.execute("INSERT INTO accounts VALUES (?, ?)", (1, 1000))
cur.execute("INSERT INTO accounts VALUES (?, ?)", (2, 500))

try:
    cur.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (200, 1))
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (200, 2))
    db.commit()
    print("Transfer successful")
except:
    db.rollback()
    print("Transfer failed")

print(cur.execute("SELECT * FROM accounts").fetchall())
db.close()
