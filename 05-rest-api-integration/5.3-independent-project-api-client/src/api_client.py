import requests
class APIClient:

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    def get_users(self, page=1, limit=5):

        url = f"{self.base_url}/users"

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params={
                    "page": page,
                    "limit": limit
                },
                timeout=5
            )

            if response.status_code == 401:
                raise Exception("Authentication failed")

            if response.status_code == 429:
                raise Exception("Too many requests")

            if response.status_code >= 400:
                raise Exception(
                    f"API error: {response.status_code}"
                )

            return response.json()

        except requests.exceptions.Timeout:
            raise Exception("Request timed out")

        except requests.exceptions.ConnectionError:
            raise Exception("Connection failed")

        except ValueError:
            raise Exception("Invalid JSON response")


if __name__ == "__main__":

    client = APIClient(
        "https://api.example.com/v1",
        "my-secret-token"
    )

    try:
        users = client.get_users(page=1, limit=5)

        print("Users:")
        print(users)

    except Exception as error:
        print("Error:", error)
