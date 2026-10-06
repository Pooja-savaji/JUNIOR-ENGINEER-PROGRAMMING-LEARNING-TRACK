import requests
from unittest.mock import patch
from src.api_client import APIClient

client = APIClient(
    "https://api.example.com/v1",
    "test-token"
)

# Test successful response
@patch("src.api_client.requests.get")
def test_success(mock_get):

    mock_get.return_value.status_code = 200

    mock_get.return_value.json.return_value = {
        "page": 1,
        "limit": 5,
        "total": 2,
        "users": [
            {
                "id": 1,
                "name": "Pooja"
            }
        ]
    }

    result = client.get_users(page=1, limit=5)
    assert result["page"] == 1
    assert result["limit"] == 5
    assert len(result["users"]) == 1


# Test authentication failure
@patch("src.api_client.requests.get")
def test_authentication_failure(mock_get):

    mock_get.return_value.status_code = 401

    try:
        client.get_users()
        assert False

    except Exception as error:
        assert str(error) == "Authentication failed"


# Test rate limit
@patch("src.api_client.requests.get")
def test_rate_limit(mock_get):

    mock_get.return_value.status_code = 429

    try:
        client.get_users()
        assert False

    except Exception as error:
        assert str(error) == "Too many requests"


# Test timeout
@patch("src.api_client.requests.get")
def test_timeout(mock_get):

    mock_get.side_effect = requests.exceptions.Timeout

    try:
        client.get_users()
        assert False

    except Exception as error:
        assert str(error) == "Request timed out"
