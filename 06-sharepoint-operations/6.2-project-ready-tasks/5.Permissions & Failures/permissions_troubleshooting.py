
def check_access(user, permission):
    required_permission = "Edit"

    if permission == required_permission:
        print(f"{user}: Access granted")
    else:
        print(f"{user}: Access denied - Permission issue")


def check_connection(connected):
    if connected:
        print("SharePoint connection successful")
    else:
        print("Connection failed - Connectivity issue")


# Simulate permission failure
check_access("Employee", "Read")

# Simulate successful access
check_access("Training Manager", "Edit")

# Simulate connectivity failure
check_connection(False)

# Simulate successful connection
check_connection(True)


# Troubleshooting guide
print("\nTroubleshooting:")
print("Access Denied → Check user permissions and access level")
print("Connection Failed → Check network, URL, and configuration")
print("Too Many Requests → Wait and retry with backoff")
