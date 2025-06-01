import os
import json
from app.config.paths import ID_STATE_DIR

os.makedirs(ID_STATE_DIR, exist_ok=True)

def get_state(user_id, key):

    path = os.path.join(ID_STATE_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            state = json.load(f)
        return state.get(key)
    return None

def set_state(user_id, key, value):

    path = os.path.join(ID_STATE_DIR, f"{user_id}.json")
    state = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            state = json.load(f)
    state[key] = value
    with open(path, "w") as f:
        json.dump(state, f, indent=2)

def delete_state(user_id):
    path = os.path.join(ID_STATE_DIR, f"{user_id}.json")
    if os.path.exists(path):
        os.remove(path)

def search_state(user_id, key):

    path = os.path.join(ID_STATE_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            state = json.load(f)
        return key in state
    return False

def delete_state_key(user_id, key):

    path = os.path.join(ID_STATE_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            state = json.load(f)
        if key in state:
            del state[key]
            with open(path, "w") as f:
                json.dump(state, f, indent=2)
