#region IMPORTS
import os
import json
from path import resource_path, data_path
from pathlib import Path

#endregion

# Path to the .JSON file (CRITICAL FOR THE PROGRAM TO WORK)
json_path = data_path("USERNAME & PASSWORD", "users.json")
default_json = resource_path("USERNAME & PASSWORD", "users.json")

if not Path(json_path).exists():
    Path(json_path).parent.mkdir(parents=True, exist_ok=True)

    with open(default_json, "r", encoding="utf-8") as src:
        content = src.read()

    with open(json_path, "w", encoding="utf-8") as dst:
        dst.write(content)

#VARIABLES
login_success = False

#region DEFINITIONS

def load_users_dict():
    with open(json_path, "r") as f:
        return json.load(f)

def save_users_dict(data):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

def get_all_users():
    data = load_users_dict()
    return list(data.values())

def username_exists(username):
    data = load_users_dict()

    for user in data.values():
        if user["username"] == username:
            return True

    return False

def add_user_data(username, display_name, password):
    data = load_users_dict()

    new_user_id = str(max((int(uid) for uid in data.keys()), default=0) + 1)
    data[new_user_id] = {
        "username": username,
        "DisplayName": display_name,
        "password": password,
        "theme": "default",
        "isAdmin": "false"
    }

    save_users_dict(data)

def delete_user_data(username):
    data = load_users_dict()

    user_id_to_delete = None
    for uid, user in data.items():
        if user["username"] == username:
            user_id_to_delete = uid
            break

    if user_id_to_delete:
        del data[user_id_to_delete]
        save_users_dict(data)
        print(f"User '{username}' deleted successfully.")
    else:
        print(f"User '{username}' not found.")

def update_user_data(username, new_display_name=None, new_password=None):
    data = load_users_dict()

    user_id_to_update = None
    for uid, user in data.items():
        if user["username"] == username:
            user_id_to_update = uid
            break

    if user_id_to_update:
        if new_display_name:
            data[user_id_to_update]["DisplayName"] = new_display_name
        if new_password:
            data[user_id_to_update]["password"] = new_password

        save_users_dict(data)
        print(f"User '{username}' updated successfully.")
    else:
        print(f"User '{username}' not found.")

def authenticate_user(username, password):
    data = load_users_dict()

    for user in data.values():
        if user["username"] == username and user["password"] == password:
            return user

    return None

#endregion

#==============================
#     STANDALONE TESTING
#==============================
if __name__ == "__main__":
    pass
