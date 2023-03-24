"""Getting data from API."""
from config import YES_NO_API_URL, ANSWER_RESPONSE_MSG, OK
from requests import get


def get_answer() -> dict:
    answer_data = {"answer": None, "forced": None, "image": None}
    response = get(YES_NO_API_URL)
    status_code = response.status_code
    if status_code != OK:
        print(f'{ANSWER_RESPONSE_MSG} {__name__} failed with status code: {status_code}')
        return answer_data
    response_data = response.json()
    if not response_data:
        print(f'{ANSWER_RESPONSE_MSG} did respond with empty content')
        return answer_data
    for key in answer_data.keys():
        answer_data[key] = response_data.get(key)
    return answer_data
