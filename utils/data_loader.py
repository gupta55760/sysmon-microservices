# utils/data_loader.py

import json
import csv
import os

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def load_test_data(filename):
    """
    Load test data from either the 'tests' or 'data' directory.
    Use subdir="data" for shared CSV/JSON test input.
    """

    data_dir = os.path.join(get_project_root(), 'tests', 'data')
    full_path = os.path.join(data_dir, filename)

    if filename.endswith(".json"):
        with open(full_path, 'r') as f:
            return json.load(f)
    elif filename.endswith(".csv"):
        with open(full_path, newline='') as f:
            reader = csv.DictReader(f)
            return list(reader)
    else:
        raise ValueError(f"Unsupported file type: {filename}")

