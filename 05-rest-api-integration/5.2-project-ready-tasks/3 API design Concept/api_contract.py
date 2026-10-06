
# Small Resource: Books
API_NAME = "Book API"
BASE_URL = "/api/v1/books"

# 1. RESOURCE
book_resource = {
    "id": 1,
    "title": "Python Basics",
    "author": "John Smith"
}

# 2. CRUD API ENDPOINTS
api_contract = {

    "CREATE": {
        "method": "POST",
        "endpoint": BASE_URL,
        "request_body": {
            "title": "Python Basics",
            "author": "John Smith"
        },
        "success_status": 201
    },

    "GET_ALL": {
        "method": "GET",
        "endpoint": BASE_URL,
        "success_status": 200
    },

    "GET_ONE": {
        "method": "GET",
        "endpoint": BASE_URL + "/{id}",
        "success_status": 200
    },

    "UPDATE": {
        "method": "PUT",
        "endpoint": BASE_URL + "/{id}",
        "request_body": {
            "title": "Advanced Python",
            "author": "John Smith"
        },
        "success_status": 200
    },

    "DELETE": {
        "method": "DELETE",
        "endpoint": BASE_URL + "/{id}",
        "success_status": 204
    }
}


# 3. PAGINATION
pagination = {
    "endpoint": BASE_URL,
    "example": "/api/v1/books?page=1&limit=5"
}


# 4. FILTERING
filtering = {
    "parameter": "author",
    "example": "/api/v1/books?author=John"
}


# 5. AUTHENTICATION HEADER
authentication = {
    "header": "Authorization",
    "value": "Bearer YOUR_TOKEN"
}


# 6. IDEMPOTENCY
idempotency = {
    "GET": True,
    "POST": False,
    "PUT": True,
    "DELETE": True
}


# 7. API VERSIONING
versioning = {
    "current_version": "/api/v1/books",
    "future_version": "/api/v2/books"
}


# 8. STATUS CODES
status_codes = {
    200: "Success",
    201: "Created",
    204: "Deleted successfully",
    400: "Bad Request",
    401: "Unauthorized",
    404: "Book Not Found",
    500: "Server Error"
}


# DISPLAY THE API CONTRACT

print("===== BOOK API CONTRACT =====")

print("\nResource:")
print(book_resource)

print("\nCRUD Endpoints:")
for name, details in api_contract.items():
    print(name, ":", details)

print("\nPagination:")
print(pagination)

print("\nFiltering:")
print(filtering)

print("\nAuthentication:")
print(authentication)

print("\nIdempotency:")
print(idempotency)

print("\nVersioning:")
print(versioning)

print("\nStatus Codes:")
print(status_codes)
