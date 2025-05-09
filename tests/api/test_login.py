# tests/api/test_login_variations.py

import pytest
from utils.data_loader import load_test_data

# Choose either CSV or JSON
TEST_DATA_FILE = "login_data_api.csv"   # or "login_data.json"

def get_login_test_data():
    data = load_test_data(TEST_DATA_FILE)
    return [
        (row["username"], row["password"], int(row["expected_status"]), row["description"])
        for row in data
    ]

@pytest.mark.parametrize(
    "username,password,expected_status,description", get_login_test_data()
)

def test_login_variant(client, username, password, expected_status, description):
    response = client.post("/api/users/login", json={"username": username, "password": password})
    assert response.status_code == expected_status, f"Failed: {description}"

