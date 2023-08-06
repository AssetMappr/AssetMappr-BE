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
        objects(objects): Collection of objects. Part of Django.
    """
    name = models.CharField("Name", max_length=240)
    description = models.CharField("Description", max_length=240)
    objects = models.Manager()

    def __str__(self):
        return str(self.name)
    
    class Meta:
        """Table for user info"""
        db_table = "assets"
