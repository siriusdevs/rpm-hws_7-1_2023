from requests import get
from config import QUOTE_API_URL, QOUTE_RESPONSE_MSG, OK


def get_quote() -> dict:
    quote_data = {
        "qotd_date": None,
        "quote": {
            "id": None,
            "dialogue": None,
            "private": None,
            "tags": None,
            "url": None,
            "favorites_count": None,
            "upvotes_count": None,
            "downvotes_count": None,
            "author": None,
            "author_permalink": None,
            "body": None
        }
    }

    response = get(QUOTE_API_URL)
    status_code = response.status_code
    if status_code != OK:
        print(f'{QOUTE_RESPONSE_MSG} {__name__} failed with status code: {status_code}')
        return quote_data
    response_data = response.json()
    if not response_data:
        print(f'{QOUTE_RESPONSE_MSG} did respond with empty content')
        return quote_data
    for key in quote_data.keys():
        quote_data[key] = response_data.get(key)
    return quote_data
