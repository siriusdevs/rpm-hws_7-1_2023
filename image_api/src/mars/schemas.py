"""Mars schemas."""
from enum import Enum


class ModelImageMars(Enum):
    """Model of path for Mars images."""

    rover_name = "rover_name"
    camera = "camera"
    url = "url"
