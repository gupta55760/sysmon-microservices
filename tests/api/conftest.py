# tests/api/conftest.py
import pytest
import httpx
import os
import sys

BASE_URL = "http://localhost:8080"

THIS_DIR = os.path.dirname(__file__)
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

THIS_DIR = os.path.join(os.path.dirname(__file__), '..', '..')
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

@pytest.fixture(scope="session")
def client():
    return httpx.Client(base_url=BASE_URL)
