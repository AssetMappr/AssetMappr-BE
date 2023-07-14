"""User app
"""
from django.apps import AppConfig


class UserConfig(AppConfig):
    """User config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
