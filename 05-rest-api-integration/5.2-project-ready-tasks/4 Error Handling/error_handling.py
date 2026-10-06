import requests
import time

URL = "https://jsonplaceholder.typicode.com/posts/1"


def get_data():
    for attempt in range(3):
        try:
            print("Attempt:", attempt + 1)

            response = requests.get(URL, timeout=3)

            if response.status_code == 429:
                print("Too many requests. Waiting...")
                time.sleep(2)
                continue

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):
                print("Invalid response.")
                return

            print("Success!")
            print(data)
            return

        except requests.exceptions.Timeout:
            print("Request timed out. Retrying...")

        except requests.exceptions.ConnectionError:
            print("Connection failed. Retrying...")

        except requests.exceptions.RequestException:
            print("Something went wrong.")
            return

        time.sleep(1)

    print("Maximum retries reached. Please try again later.")


get_data()
