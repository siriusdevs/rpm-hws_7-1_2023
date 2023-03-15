"""User schemas."""
import datetime
from enum import Enum
from pydantic import BaseModel


class ModelImageUser(Enum):
    """Model of path for user images."""

    title = "title"
    explanation = "explanation"
    date = "date"
    data = "data"
    url = "url"


class Image(BaseModel):
    """Model for validation image."""

    title: str
    explanation: str
    date: datetime.date = datetime.date.today()


class UserImage(BaseModel):
    """Model for validation user image."""

    id: int
    title: str
    explanation: str
    date: datetime.date
    url: str
    user_name: str
