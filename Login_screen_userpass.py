#region IMPORTS
import os
import subprocess
import json
from path import resource_path, asset_path

#endregion

# Path to the .JSON file (CRITICAL FOR THE PROGRAM TO WORK)
json_path = resource_path("USERNAME & PASSWORD", "users.json")

#VARIABLES
login_success = False

#region DEFINITIONS

def load_all_user_data():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    
    with open(json_path, 'r') as f:
        data = json.load(f)
        print(data)
        #Shows all the data in the .JSON file

def load_user_data(username):
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

    with open(json_path, "r") as f:
        data = json.load(f)

        for user in data.values():
            if user["username"] == username:
                print("Matched user:", user["username"])
                print("Display Name:", user["DisplayName"])

    return None

def add_user_data(username, display_name, password):
    with open(json_path, "r") as f:
        data = json.load(f)

    new_user_id = str(max(int(uid) for uid in data.keys()) + 1)
    data[new_user_id] = {
        "username": username,
        "DisplayName": display_name,
        "password": password
    }

    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

def delete_user_data(username):
    with open(json_path, "r") as f:
        data = json.load(f)

    user_id_to_delete = None
    for uid, user in data.items():
        if user["username"] == username:
            user_id_to_delete = uid
            break

    if user_id_to_delete:
        del data[user_id_to_delete]
        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"User '{username}' deleted successfully.")
    else:
        print(f"User '{username}' not found.")

def update_user_data(username, new_display_name=None, new_password=None):
    with open(json_path, "r") as f:
        data = json.load(f)

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

        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"User '{username}' updated successfully.")
    else:
        print(f"User '{username}' not found.")

def login_user(username, password):
    with open(json_path, "r") as f:
        data = json.load(f)

    for user in data.values():
        if user["username"] == username and user["password"] == password:
            print(f"Login successful! Welcome, {user['DisplayName']}!")
            return True

    print("Login failed: Invalid username or password.")
    return False


def authenticate_user(username, password):
    with open(json_path, "r") as f:
        data = json.load(f)

    for user in data.values():
        if user["username"] == username and user["password"] == password:
            return user

    return None

#endregion

standalone = False
#==============================
#     STANDALONE TESTING
#==============================
if __name__ == "__main__":
    standalone = True
else:
    standalone = False
