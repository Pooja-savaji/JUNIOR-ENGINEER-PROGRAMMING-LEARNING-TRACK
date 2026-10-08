def get_user_name(users, user_id):
    return users[user_id]["name"]

users = {
    1: {"name": "Pooja"},
    2: {"name": "Rahul"}
}
print(get_user_name(users, 3))

Bug: User ID 3 does not exist.
