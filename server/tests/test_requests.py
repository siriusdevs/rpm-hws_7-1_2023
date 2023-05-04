from requests import get
OK = 200
CREATED = 201
URL = 'http://127.0.0.1:8001/students'
headers = {
    'Set-cookie': '123',
}


def test_requests():
    assert get(URL, headers=headers).status_code == OK


if __name__ == '__main__':
    # here you should use setup_env and setup_db if it was not used before
    test_requests()
