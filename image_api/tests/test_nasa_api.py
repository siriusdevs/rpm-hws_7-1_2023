"""Tests for nasa api."""
from os import getenv


from fastapi.testclient import TestClient

from http_config import HTTP_UNPROCESS_ENTITY, HTTP_OK
from src.main import app

II = 2

client = TestClient(app)
TEST_USER = getenv("TEST_USER", default="test")
TEST_TOKEN = getenv("TEST_TOKEN", default="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
USER_TOKEN = f"{TEST_USER}_{TEST_TOKEN}"
IMAGE_ID = None


def test_for_test():
    assert II == 2


def test_read_main():
    response = client.get("/")
    assert response.status_code == HTTP_OK


def test_get_nasa_today_bad():
    response = client.get('/image/nasa/')
    assert response.status_code == HTTP_UNPROCESS_ENTITY


def test_get_nasa_today():
    response = client.get(f'/image/nasa/?token={USER_TOKEN}')
    assert response.status_code == HTTP_OK


def test_get_nasa_random():
    response = client.get(f'/image/nasa/random/?token={USER_TOKEN}')
    assert response.status_code == HTTP_OK


def test_get_mars_today_bad():
    response = client.get('/image/mars/')
    assert response.status_code == HTTP_UNPROCESS_ENTITY


def test_get_mars_today():
    response = client.get(f'/image/mars/?token={USER_TOKEN}')
    assert response.status_code == HTTP_OK
