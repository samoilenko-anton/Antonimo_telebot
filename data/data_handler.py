import json
import os
from datetime import datetime, timedelta

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user_response(user_id):
    data = load_data()
    user_id = str(user_id)

    if user_id not in data:
        return None

    timestamp = datetime.strptime(data[user_id]["timestamp"], "%Y-%m-%d %H:%M:%S")
    if datetime.now() - timestamp < timedelta(hours=1):
        return data[user_id]["response"]

    return None

def store_user_response(user_id, response):
    data = load_data()
    user_id = str(user_id)

    data[user_id] = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "response": response
    }

    save_data(data)