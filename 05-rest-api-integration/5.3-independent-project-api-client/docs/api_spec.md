
Base URL:
https://api.example.com/v1

Authentication:
Use a Bearer token.

Header:
Authorization: Bearer YOUR_TOKEN

Endpoint:
GET /users

Query Parameters:
page  - page number
limit - number of users per page

Example:
GET /users?page=1&limit=5

Success:
200 OK

Response:
{
    "page": 1,
    "limit": 5,
    "total": 10,
    "users": [
            {
            "id": 1,
            "name": "Pooja",
            "email": "pooja@example.com"
        }
    ]
}
Errors:
400 - Invalid request
401 - Authentication failed
429 - Too many requests
500 - Server error
