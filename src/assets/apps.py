"""
This module defines applicatio configs.

Author: Shashank Shekhar
"""

from django.apps import AppConfig


class AssetsConfig(AppConfig):
    """
    Asset Configurations.

    Attributes:
        default_auto_field (string): Default auto field.
        name (string): Name
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assets'
