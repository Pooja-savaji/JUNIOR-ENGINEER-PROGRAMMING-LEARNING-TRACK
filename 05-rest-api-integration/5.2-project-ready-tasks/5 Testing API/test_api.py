import requests
import pytest
from unittest.mock import patch

def get_user():
    return requests.get(
        "https://example.com/users/1",
        timeout=3
    )

# 1. Success case
@patch("requests.get")
def test_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "id": 1,
        "name": "Pooja"
    }

    response = get_user()

    assert response.status_code == 200
    assert response.json()["id"] == 1


# 2. Validation failure
@patch("requests.get")
def test_validation_failure(mock_get):
    mock_get.return_value.status_code = 400

    response = get_user()

    assert response.status_code == 400


# 3. Authentication failure
@patch("requests.get")
def test_auth_failure(mock_get):
    mock_get.return_value.status_code = 401

    response = get_user()

    assert response.status_code == 401


# 4. Timeout
@patch("requests.get")
def test_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout

    with pytest.raises(requests.exceptions.Timeout):
        get_user()
