from django.db import models


class Asset(models.Model):
    name = models.CharField("Name", max_length=240)
    description = models.CharField("Description", max_length=240)

    def __str__(self):
        return str(self.name)
