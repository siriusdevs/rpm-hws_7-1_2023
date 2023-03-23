"""Parse data from APT."""
from requests import get
from config import API_URL, OK, CHARACTER_MSG, AUTH, CHARACTER_META
from dotenv import load_dotenv
from os import getenv


load_dotenv()
API_KEY = getenv('API_KEY')


def get_character(query: dict) -> dict:
    """Fill dict with API data.

    Args:
        query : dict - data from API
    """
    character_data = {
        'race': None,
        'gender': None,
        'birth': None,
        'spouse': None,
        'death': None,
        'realm': None,
        'name': 'Gandalf'
    }
    try:
        name = query.get('name')
    except Exception:
        print(f'{CHARACTER_MSG} failed to get name from query, defaults to Gandalf')
        CHARACTER_META['name'] = 'Gandalf'
        api_request = CHARACTER_META
    else:
        CHARACTER_META['name'] = name
        api_request = CHARACTER_META
        character_data['name'] = name
    response = get(API_URL, params=api_request, headers={AUTH: f'Bearer {API_KEY}'})
    if response.status_code != OK:
        print(f'{CHARACTER_MSG} failed with status code: {response.status_code}')
        return character_data
    response_data = response.json()
    if not response_data:
        print(f'{CHARACTER_MSG} api did respond with empty content')
        return character_data
    docs = response_data.get('docs')
    if not docs:
        print(f'{CHARACTER_MSG} api did not provide character metadata')
        character_data['death'] = 'Death: {0}'.format(character_data['death'])
        return character_data
    for key in character_data.keys():
        api_response: str = docs[0].get(key)
        if key == 'spouse' and api_response == '':
            character_data[key] = 'Unmarried'
        elif key == 'death':
            if api_response.startswith('Still alive'):
                character_data[key] = api_response
            else:
                character_data[key] = f'Death: {api_response}'
        else:
            character_data[key] = api_response
    return character_data
