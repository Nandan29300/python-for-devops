# Day 02 – Automating System Tasks with Python


import requests
import json

def fetch_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def process_users(users):
    processed = []
    for user in users:
        info = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "city": user["address"]["city"]
        }
        processed.append(info)
    return processed

def save_to_json(data, filename="output.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def main():
    print("Fetching users from JSONPlaceholder...")
    users = fetch_users()
    processed = process_users(users)
    print("\nProcessed User Data:")
    for user in processed:
        print(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, City: {user['city']}")
    save_to_json(processed)
    print("\nData saved to output.json")

if __name__ == "__main__":
    main()
