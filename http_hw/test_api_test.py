from api import app
from config import NOT_FOUND_TEST, FORBIDDEN_TEST, PUT_OK, BAD_REQUEST_TEST,\
    POST_OK, HOST, PORT, DELETE_OK, DEMO_TOKEN, CURRENT_RESPONSE, OK, CREATED
from fastapi.testclient import TestClient


client = TestClient(app)
json = {"Authorization": "daniil {0}".format(DEMO_TOKEN)}
incorrect_json = {"Authorization": "danil {0}".format(DEMO_TOKEN)}


def test_get():
    response = client.get("/quotes/?id=2", headers=json)
    assert response.status_code == OK
    assert response.json() == CURRENT_RESPONSE


def test_get2():
    response = client.get("/quotes/?id=100", headers=json)
    assert response.status_code == NOT_FOUND_TEST['detail']['code']
    assert response.json() == NOT_FOUND_TEST


def test_get3():
    response = client.get("/quotes/?id=6", headers=incorrect_json)
    assert response.status_code == FORBIDDEN_TEST['detail']['code']
    assert response.json() == FORBIDDEN_TEST


def test_get4():
    response = client.get("/quotes/?i=6", headers=json)
    assert response.status_code == BAD_REQUEST_TEST['detail']['code']
    assert response.json() == BAD_REQUEST_TEST


def test_put():
    test = '&author=Maksim+Bezborodov&body=What does it mean? It means that you are a hole.'
    response = client.put("/quotes?id=2{0}".format(test), headers=json)
    assert response.status_code == OK
    assert response.json() == PUT_OK


def test_put2():
    response = client.put("/quotes?id=100&author=Coca&body=Cola", headers=json)
    assert response.status_code == NOT_FOUND_TEST['detail']['code']
    assert response.json() == NOT_FOUND_TEST


def test_put3():
    response = client.put("/quotes?id=6&autho=Coca&body=Cola", headers=json)
    assert response.status_code == BAD_REQUEST_TEST['detail']['code']
    assert response.json() == BAD_REQUEST_TEST


def test_put4():
    response = client.put("/quotes?id=6&author=Coca&body=Cola", headers=incorrect_json)
    assert response.status_code == FORBIDDEN_TEST['detail']['code']
    assert response.json() == FORBIDDEN_TEST


def test_post():
    response = client.post("/quotes", json={"author": "Coca", "body": "Cola"}, headers=json)
    POST_OK["url"] = "http://{0}:{1}/quotes?id=6".format(HOST, PORT)
    assert response.status_code == CREATED
    assert response.json() == POST_OK


def test_post2():
    response = client.post("/quotes", json={"author": "Coca", "body": "Cola"}, headers=json)
    assert response.status_code == BAD_REQUEST_TEST['detail']['code']
    assert response.json() == BAD_REQUEST_TEST


def test_post3():
    response = client.post("/quotes", json={"author": "Coca", "body": "Cola"}, headers=incorrect_json)
    assert response.status_code == FORBIDDEN_TEST['detail']['code']
    assert response.json() == FORBIDDEN_TEST


def test_post4():
    response = client.post("/quotes", json={"author": "Coca", "body": "Cola"}, headers=json)
    assert response.status_code == BAD_REQUEST_TEST['detail']['code']
    assert response.json() == BAD_REQUEST_TEST


def test_delete():
    response = client.delete("/quotes?id=1", headers=json)
    assert response.status_code == OK
    assert response.json() == DELETE_OK


def test_delete2():
    response = client.delete("/quotes?id=1", headers=incorrect_json)
    assert response.status_code == FORBIDDEN_TEST['detail']['code']
    assert response.json() == FORBIDDEN_TEST


def test_delete3():
    response = client.delete("/quotes?id=100", headers=json)
    assert response.status_code == NOT_FOUND_TEST['detail']['code']
    assert response.json() == NOT_FOUND_TEST


def test_delete4():
    response = client.delete("/quotes?i=100", headers=json)
    assert response.status_code == BAD_REQUEST_TEST['detail']['code']
    assert response.json() == BAD_REQUEST_TEST
