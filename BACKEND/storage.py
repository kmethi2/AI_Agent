import os
import json
from datetime import datetime

# Folder where we save all data
DATA_DIR = "data"

# Ensure the data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def save_data(filename, data):
    """
    Saves any Python object (dict, list, etc.) as JSON in the /data folder.
    Automatically appends a timestamp to the filename if needed.
    """
    if not filename.endswith(".json"):
        filename += ".json"
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ Saved data to {filepath}")

def load_data(filename):
    """
    Loads JSON data from /data folder. Returns None if file doesn't exist.
    """
    if not filename.endswith(".json"):
        filename += ".json"
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"⚠️ File {filepath} not found.")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_daily_headlines(headlines):
    """
    Saves today's headlines with date in filename.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    save_data(f"headlines_{date_str}", headlines)

def save_daily_deep_dive(deep_dive):
    """
    Saves today's deep dive with date in filename.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    save_data(f"deep_dive_{date_str}", deep_dive)

# Quick test
if __name__ == "__main__":
    test_data = {"example": "This is a test"}
    save_data("test_file", test_data)
    loaded = load_data("test_file")
    print("Loaded:", loaded)
