"""
This module defines Serilaizers.

Author: Shashank Shekhar
"""

from rest_framework import serializers
from .models import Asset


class AssetSerializer(serializers.ModelSerializer):
    """
    Asset Serializer.
    """
    class Meta:
        """
        Meta Info for class.
        """
        model = Asset
        fields = ('pk', 'name', 'description')
