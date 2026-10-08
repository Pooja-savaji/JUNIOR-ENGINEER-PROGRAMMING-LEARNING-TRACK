import json
import os

def load_users():
    with open("data/users.json", "r") as file:
        return json.load(file)

def calculate_total(price, quantity):
    return price + quantity

def get_email(user):
    return user["email"]

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

def get_app_mode():
    return os.environ["APP_MODE"]

def main():
    users = load_users()
    print("Total:", calculate_total(100, 2))
    print("Email:", get_email({"name": "Pooja"}))
    print("Average:", calculate_average([]))
    print("Mode:", get_app_mode())
    print("Users:", users)

if __name__ == "__main__":
    main()
