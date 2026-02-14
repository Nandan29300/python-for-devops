import requests
import json

def fetch_users(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        print(f"API request failed: {exc}")
        return []

def process_users(users):
    processed = []
    for user in users:
        info = {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "city": user.get("address", {}).get("city")
        }
        processed.append(info)
    return processed

def save_to_json(data, filename="output.json"):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as exc:
        print(f"Failed to write JSON file: {exc}")

def main():
    api_url = "https://jsonplaceholder.typicode.com/users"

    print("Fetching users from API...")
    users = fetch_users(api_url)
    if not users:
        print("No users to process. Exiting.")
        return

    processed = process_users(users)
    print("\nProcessed User Data:")
    for user in processed:
        print(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, City: {user['city']}")
    save_to_json(processed)
    print("\nData saved to output.json")

if __name__ == "__main__":
    main()