"""Nasa entrypoints."""
import datetime
from typing import Union

from fastapi import APIRouter, HTTPException

from http_config import HTTP_FORBIDDEN
from src.database import check_token
from src.nasa_api import get_apod_date_image, get_apod_random_image
from .schemas import ModelImageNasa

router = APIRouter(
    prefix="/image/nasa",
    tags=["Nasa Image"]
)


@router.get("/{model_image}")
@router.get("/")
def image_nasa_today(token: str, model_nasa: ModelImageNasa | None = None):
    """Returns a Nasa photo of today.

    Args:
        token (str): for auth user.
        model_nasa (ModelImageNasa): allowed path.
    """
    if not model_nasa:
        return image_nasa(token, datetime.date.today())

    return {model_nasa.value: image_nasa(token, datetime.date.today()).get(model_nasa.value)}


@router.get("/random/{model_image}")
@router.get("/random/")
def random_image_nasa(token: str, model_nasa: ModelImageNasa | None = None):
    """Returns a random Nasa photo.

    Args:
        token (str): for auth user.
        model_nasa (ModelImageMars): allowed path.

    Raises:
        HTTPException: Forbidden if wrong token.
    """
    if not check_token(token):
        raise HTTPException(status_code=HTTP_FORBIDDEN, detail="Wrong token")
    if not model_nasa:
        return get_apod_random_image()
    return {model_nasa.value: get_apod_random_image().get(model_nasa.value)}


@router.get("/{date}/{model_image}")
@router.get("/{date}/")
def image_nasa(token: str, date: Union[datetime.date, None] = None, model_nasa: ModelImageNasa | None = None):
    """Returns a Nasa photo of the day.

    Args:
        token (str): for auth user.
        model_nasa (ModelImageMars): allowed path.
        date (datetime.date): data of photo, if null used today's date in format YYYY-MM-DD

    Raises:
        HTTPException: Forbidden if wrong token.
    """
    if not check_token(token):
        raise HTTPException(status_code=HTTP_FORBIDDEN, detail="Wrong token")
    if not date:
        date = datetime.date.today()
    if not model_nasa:
        return get_apod_date_image(date)

    return {model_nasa.value: get_apod_date_image(date).get(model_nasa.value)}
