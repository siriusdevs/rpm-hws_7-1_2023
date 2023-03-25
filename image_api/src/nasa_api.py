"""Some functions to work with nasa api."""
import datetime
import random
from os import getenv

from config import MARS_IMAGE, NASA_IMAGE
from requests import get
from dotenv import load_dotenv

load_dotenv()
NASA_API = getenv('NASA_API', default="DEMO_KEY")


def get_mars_date_image(date: datetime.date) -> dict:
    """Returns a Mars photo in dict from nasa api.

    Args:
        date (datetime.date): photos' date.
    """
    requests = get(MARS_IMAGE.format(api_key=NASA_API, parameters=f"earth_date={date}"))
    photos = requests.json().get("photos")
    random.shuffle(photos)
    if photos:
        photo = photos[0]
        return {"rover_name": photo.get("rover").get("name"), "camera": photo.get("camera").get("full_name"),
                "url": photo.get('img_src')}

    return {"rover_name": "null", "camera": "null", "url": "null"}


def get_apod_random_image() -> dict:
    """Returns a random Nasa photo in dict from nasa api."""
    requests = get(NASA_IMAGE.format(api_key=NASA_API, parameters="count=1"))
    json = requests.json()[0]
    return {"date": json.get("date"), "title": json.get('title'), "explanation": json.get("explanation"),
            "url": json.get("hdurl")}


def get_apod_date_image(date: str) -> dict:
    """Returns Mars photo in dict from nasa api.

    Args:
        date (str): photos' date.
    """
    requests = get(NASA_IMAGE.format(api_key=NASA_API, parameters=f"date={date}"))
    json = requests.json()
    return {"date": json.get("date"), "title": json.get('title'), "explanation": json.get("explanation"),
            "url": json.get("hdurl")}
