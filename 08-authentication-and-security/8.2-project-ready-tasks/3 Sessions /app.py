users = {
    "pooja": "admin",
    "rahul": "user"
}

def check_access(username, screen):
    role = users.get(username)

    if role is None:
        return "User not found"

    if screen == "admin" and role != "admin":
        return "Access denied"

    return "Access allowed"

print(check_access("pooja", "admin"))
print(check_access("rahul", "admin"))
print(check_access("rahul", "user"))
