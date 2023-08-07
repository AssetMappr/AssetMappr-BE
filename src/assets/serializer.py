"""
This module defines Serilaizers.

Author: Shashank Shekhar
"""

from rest_framework import serializers
from .models import Assets


class AssetSerializer(serializers.ModelSerializer):
    """
    Asset Serializer.
    """
    class Meta:
        """
        Meta Info for class.
        """
        model = Assets
        fields = ("id", 
                  "name",
                  "type",
                  "community_geo_id",
                  "community_name",
                  "community_id",
                  "source_id",
                  "user_id",
                  "category_id",
                  "description",
                  "website",
                  "latitude",
                  "longitude",
                  "address",
                  "timestamp",
                  "status")
