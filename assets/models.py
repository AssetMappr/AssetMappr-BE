"""
This module defines models.

Author: Shashank Shekhar
"""

from django.db import models


class Asset(models.Model):
    """
    Asset ORM model.

    Attributes:
        name (string): Name of the asset.
        description (string): Description of the asset.
    """
    name = models.CharField("Name", max_length=240)
    description = models.CharField("Description", max_length=240)

    def __str__(self):
        return str(self.name)
