"""Tests for user image."""

from os import getenv
from pathlib import Path

from fastapi.testclient import TestClient

from http_config import HTTP_OK, HTTP_CREATE, HTTP_FORBIDDEN
from src.main import app

II = 2

client = TestClient(app)
TEST_USER = getenv("TEST_USER", default="test")
TEST_TOKEN = getenv("TEST_TOKEN", default="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
USER_TOKEN = f"{TEST_USER}_{TEST_TOKEN}"
IMAGE_ID = None


def test_user_post_bad():
    with open(Path("tests/test_image.png").absolute(), 'rb') as test_file:
        response = client.post(
            f"/image/user/{TEST_USER}2/?token={USER_TOKEN}",  # wrong user
            files={"upload_file": ("test.png", test_file, "image/png")},
            params={"title": "test_image", "explanation": "image for testing"}
        )
    assert response.status_code == HTTP_FORBIDDEN


def test_user_post():
    global IMAGE_ID
    with open(Path("tests/test_image.png").absolute(), 'rb') as test_file:
        response = client.post(
            f"/image/user/{TEST_USER}/?token={USER_TOKEN}",
            files={"upload_file": ("test.png", test_file, "image/png")},
            params={"title": "test_image", "explanation": "image for testing"}
        )
        IMAGE_ID = response.json().get("id")
    assert response.status_code == HTTP_CREATE


def test_user_get():
    response = client.delete(f"/image/user/{TEST_USER}/{IMAGE_ID}/?token={USER_TOKEN}")
    assert response.status_code == HTTP_OK


def test_user_delete():
    response = client.delete(f"/image/user/{TEST_USER}/{IMAGE_ID}/?token={USER_TOKEN}")
    assert response.status_code == HTTP_OK
