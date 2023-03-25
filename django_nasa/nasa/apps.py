"""Nasa app config."""
from django.apps import AppConfig


class NasaConfig(AppConfig):
    """Nasa config class."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nasa'
