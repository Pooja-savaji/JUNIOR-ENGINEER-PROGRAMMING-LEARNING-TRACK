import os
import socket

def calculate_total(price, quantity):
    return price + quantity
price = 100
quantity = 2
print("Total:", calculate_total(price, quantity))

database_url = os.getenv("DATABASE_URL")
if database_url is None:
    print("DATABASE_URL is missing")
else:
    print("Database configuration found")

host = "localhost"
port = 9999
try:
    socket.create_connection((host, port), timeout=2)
    print("Server is available")

except OSError:
    print("Server is not reachable"
