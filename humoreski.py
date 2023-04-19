from requests import get
from config import API_URL


def get_humoreska() -> dict:
    humoreska_data = {
        'joke': None,
    }
    response = get(API_URL)
    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            humoreska_data = response_data
    else:
        print('ANECDOT API failed with status code: {}'.format(response.status_code))
    return humoreska_data
