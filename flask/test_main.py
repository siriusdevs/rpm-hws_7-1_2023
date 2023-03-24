from main import app
import pytest
from config import TOKEN, OK, SUCCEEDED


@pytest.fixture(name="client_for_test")
def test_client():
    with app.test_client() as client:
        yield client


def test_get_index(client_for_test):
    response = client_for_test.get('/')
    assert response.status_code == OK


def test_fill_index(client_for_test):
    data_for_test = {
        "id": 101,
        "source_to_img": "/static/images/miche_tshort.png",
        "name": "DJ Miche Collection",
        "price": 99.99,
        "description": "Dictator Miche.",
        "featured_products": True
    }
    headers = {
        "Authorization": TOKEN
    }
    response = client_for_test.post('/index/create', json=data_for_test, headers=headers)
    assert response.status_code == OK


def test_update_index(client_for_test):
    data_for_test = {
        "id": 101,
        "name": "Test name",
        "price": 999.9,
        "source_to_img": "test"
    }
    headers = {
        "Authorization": TOKEN
    }
    response = client_for_test.put('/index/update', json=data_for_test, headers=headers)
    assert response.status_code == SUCCEEDED


def test_delete_from_index(client_for_test):
    data_for_test = {
        "id": 101
    }
    headers = {
        "Authorization": TOKEN
    }
    response = client_for_test.delete('/index/delete', json=data_for_test, headers=headers)
    assert response.status_code == SUCCEEDED
