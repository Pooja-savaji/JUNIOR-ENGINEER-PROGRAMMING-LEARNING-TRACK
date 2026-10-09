import json
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    app_folder = Path(sys.executable).parent
else:
    app_folder = Path(__file__).resolve().parent

config_file = app_folder / "config.json"

def main():
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            config = json.load(file)

        print(config["app_name"])
        print(config["message"])

    except FileNotFoundError:
        print("Error: config.json not found.")

    except json.JSONDecodeError:
        print("Error: config.json contains invalid JSON.")

if __name__ == "__main__":
    main()
