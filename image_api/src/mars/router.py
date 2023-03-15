"""Mars entrypoints."""
import datetime
from typing import Union

from fastapi import APIRouter, HTTPException

from http_config import HTTP_FORBIDDEN
from src.database import check_token
from src.mars.schemas import ModelImageMars
from src.nasa_api import get_mars_date_image

router = APIRouter(
    prefix="/image/mars",
    tags=["Mars Image"]
)


@router.get("/{model_mars}")
@router.get("/")
def image_mars_today(token: str, model_mars: ModelImageMars | None = None):
    """Returns a Mars photo of today.

    Args:
        token (str): for auth user.
        model_mars (ModelImageMars): allowed path.
    """
    if not model_mars:
        return image_mars(token, datetime.date.today())
    return {model_mars.value: image_mars(token, datetime.date.today()).get(model_mars.value)}


@router.get("/{date}/{model_mars}")
@router.get("/{date}/")
def image_mars(token: str, date: Union[datetime.date, None] = None, model_mars: ModelImageMars | None = None):
    """Returns a random Mars photo of the day.

    Args:
        token (str): for auth user.
        model_mars (ModelImageMars): allowed path.
        date (datetime.date): data of photo, if null used today's date in format YYYY-MM-DD

    Raises:
        HTTPException: Forbidden if wrong token.
    """
    if not check_token(token):
        raise HTTPException(status_code=HTTP_FORBIDDEN, detail="Wrong token")

    if not date:
        date = datetime.date.today()
    if not model_mars:
        return get_mars_date_image(date)
    return {model_mars.value: get_mars_date_image(date).get(model_mars.value)}
