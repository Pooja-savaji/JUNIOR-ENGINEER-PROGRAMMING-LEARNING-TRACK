import requests
BASE_URL = "https://jsonplaceholder.typicode.com"

# 1. GET Request - Get one post
print("===== 1. GET REQUEST =====")
url = f"{BASE_URL}/posts/1"
response = requests.get(url)
print("Method: GET")
print("URL:", response.url)
print("Status Code:", response.status_code)
print("Response:")

if response.status_code == 200:
    print(response.json())
else:
    print("Request failed")

# 2. GET Request with Query Parameter
print("\n===== 2. QUERY PARAMETER =====")
url = f"{BASE_URL}/posts"
params = {
    "userId": 1
}

response = requests.get(url, params=params)

print("Method: GET")
print("URL:", response.url)
print("Status Code:", response.status_code)
print("Response:")

if response.status_code == 200:
    posts = response.json()

    for post in posts[:2]:
        print(post)
else:
    print("Request failed")

# 3. GET Request with Path Parameter
print("\n===== 3. PATH PARAMETER =====")
post_id = 2
url = f"{BASE_URL}/posts/{post_id}"
response = requests.get(url)

print("Method: GET")
print("URL:", response.url)
print("Status Code:", response.status_code)
print("Response:")

if response.status_code == 200:
    print(response.json())
else:
    print("Request failed")

# 4. POST Request - Create a new post
print("\n===== 4. POST REQUEST =====")
url = f"{BASE_URL}/posts"
data = {
    "title": "My First API Test",
    "body": "I am learning HTTP basics using Python.",
    "userId": 1
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(
    url,
    json=data,
    headers=headers
)

print("Method: POST")
print("URL:", response.url)
print("Status Code:", response.status_code)
print("Response:")

if response.status_code == 201:
    print(response.json())
else:
    print("Request failed")

# 5. Response Headers
print("\n===== 5. RESPONSE HEADERS =====")
print("Content-Type:", response.headers.get("Content-Type"))
print("Server:", response.headers.get("Server", "Not available"))

# 6. Status Code Explanation

print("\n===== 6. STATUS CODE =====")
status_code = response.status_code

if status_code == 200:
    print("200 - Request successful")

elif status_code == 201:
    print("201 - Resource created successfully")

elif status_code == 400:
    print("400 - Bad request")

elif status_code == 401:
    print("401 - Unauthorized")

elif status_code == 404:
    print("404 - Resource not found")

elif status_code == 500:
    print("500 - Server error")

else:
    print("Status Code:", status_code)
