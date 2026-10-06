import requests
BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10

def get_post(post_id):
    """Get a post using GET request."""
    url = f"{BASE_URL}/posts/{post_id}"

    try:
        response = requests.get(url, timeout=TIMEOUT)

        if response.status_code == 200:
            return response.json()

        print("GET Error:", response.status_code)
        return None

    except requests.exceptions.Timeout:
        print("GET request timed out.")
        return None

    except requests.exceptions.RequestException as error:
        print("GET request failed:", error)
        return None


def create_post(title, body, user_id):
    """Create a new post using POST request."""
    url = f"{BASE_URL}/posts"

    data = {
        "title": title,
        "body": body,
        "userId": user_id
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=TIMEOUT
        )

        if response.status_code == 201:
            return response.json()

        print("POST Error:", response.status_code)
        return None

    except requests.exceptions.Timeout:
        print("POST request timed out.")
        return None

    except requests.exceptions.RequestException as error:
        print("POST request failed:", error)
        return None


def update_post(post_id, title, body, user_id):
    """Update a post using PUT request."""
    url = f"{BASE_URL}/posts/{post_id}"

    data = {
        "title": title,
        "body": body,
        "userId": user_id
    }

    try:
        response = requests.put(
            url,
            json=data,
            timeout=TIMEOUT
        )

        if response.status_code == 200:
            return response.json()

        print("PUT Error:", response.status_code)
        return None

    except requests.exceptions.Timeout:
        print("PUT request timed out.")
        return None

    except requests.exceptions.RequestException as error:
        print("PUT request failed:", error)
        return None


def delete_post(post_id):
    """Delete a post using DELETE request."""
    url = f"{BASE_URL}/posts/{post_id}"

    try:
        response = requests.delete(
            url,
            timeout=TIMEOUT
        )

        if response.status_code == 200:
            return True

        print("DELETE Error:", response.status_code)
        return False

    except requests.exceptions.Timeout:
        print("DELETE request timed out.")
        return False

    except requests.exceptions.RequestException as error:
        print("DELETE request failed:", error)
        return False

# MAIN PROGRAM


print("================================")
print("     PYTHON HTTP CLIENT")
print("================================")


# 1. GET
print("\n--- GET REQUEST ---")
post = get_post(1)

if post:
    print("Post ID:", post["id"])
    print("Title:", post["title"])
    print("Body:", post["body"])


# 2. POST
print("\n--- POST REQUEST ---")

new_post = create_post(
    "My First API Client",
    "I am learning HTTP requests in Python.",
    1
)

if new_post:
    print("Created Post:")
    print(new_post)


# 3. PUT
print("\n--- PUT REQUEST ---")

updated_post = update_post(
    1,
    "Updated API Post",
    "This post was updated using Python.",
    1
)

if updated_post:
    print("Updated Post:")
    print(updated_post)


# 4. DELETE
print("\n--- DELETE REQUEST ---")

deleted = delete_post(1)

if deleted:
    print("Post deleted successfully.")
else:
    print("Post deletion failed.")


print("\n================================")
print("        TASK COMPLETED")
print("================================")
