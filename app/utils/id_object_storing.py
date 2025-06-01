import os
import json
from app.config.paths import ID_MEMORY_DIR

os.makedirs(ID_MEMORY_DIR, exist_ok=True)

def get_key(user_id, key):
    path = os.path.join(ID_MEMORY_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            state = json.load(f)
        return state.get(key)
    return None

def set_key(user_id, key, value):
    path = os.path.join(ID_MEMORY_DIR, f"{user_id}.json")
    state = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            state = json.load(f)
    state[key] = value
    with open(path, "w") as f:
        json.dump(state, f, indent=2)

def delete_key(user_id):
    path = os.path.join(ID_MEMORY_DIR, f"{user_id}.json")
    if os.path.exists(path):
        os.remove(path)

def search_key(user_id, key):
    path = os.path.join(ID_MEMORY_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            state = json.load(f)
        return key in state
    return False

def delete_state_key(user_id, key):
    path = os.path.join(ID_MEMORY_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            state = json.load(f)
        if key in state:
            del state[key]
            with open(path, "w") as f:
                json.dump(state, f, indent=2)

def append_key(user_id, key, appended_value):
    current_value = get_key(user_id, key)
    if current_value is None:
        new_value = appended_value
    else:
        try:
            new_value = current_value + appended_value
        except TypeError:
            raise TypeError(f"Cannot append value of type {type(appended_value)} "
                            f"to existing value of type {type(current_value)} with '+'")
    set_key(user_id, key, new_value)
