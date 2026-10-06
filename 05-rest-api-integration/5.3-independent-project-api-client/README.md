
# 5.3 Independent Project - API Client

## About
This project is a simple API client built in Python. It demonstrates how to work with an unfamiliar API using its documentation.
The client supports authentication, pagination, timeout handling, API errors, and mocked tests.


## Topics Covered

- API documentation
- API client
- Authentication
- Bearer token
- Pagination
- Query parameters
- Timeout handling
- Connection errors
- API error handling
- Rate limiting
- JSON responses
- Mocking HTTP requests
- API testing with pytest

## What I Practiced

- Reading an API specification
- Creating a Python API client
- Sending authenticated HTTP requests
- Using pagination with `page` and `limit`
- Handling common API failures
- Creating mock API responses
- Testing API code without using a live service

## How to Run

Install the required packages: pip install requests pytest
Run the API client: python src/api_client.py
Run the tests: pytest

## Expected Test Result
4 passed


## Learning Goal
The goal of this challenge is to understand how to integrate an unfamiliar API from its documentation and write reliable tests using mocked responses.

## Result
The API client was implemented with authentication, pagination, and error handling. Success, authentication failure, rate-limit, and timeout cases were tested without depending on a live API.
