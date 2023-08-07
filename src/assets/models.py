"""
This module defines models.

Author: Shashank Shekhar, Niranjan Kumawat
"""

from django.db import models


class Categories(models.Model):
    """
    Categories ORM model.

    Attributes:
        id (int): Category ID
        category (string): Category
        description (string): Description of the category.
        objects(objects): Collection of objects. Part of Django.
    """
    id = models.AutoField(primary_key=True, verbose_name="Category ID")
    category = models.CharField(
        max_length=255,
        null=False,
        verbose_name="Category")
    description = models.TextField(verbose_name="Category's description")

    objects = models.Manager()

    class Meta:
        """Table for assets"""
        db_table = "asset_categories"


class RatingValues(models.Model):
    """
    Rating Values ORM model.

    Attributes:
        id (int): ID
        value (string): Value
        weight (smallint): Description of the category.
        objects(objects): Collection of objects. Part of Django.
    """
    id = models.AutoField(primary_key=True, verbose_name="Value ID")
    category = models.CharField(
        max_length=255,
        null=False,
        verbose_name="Value")
    weight = models.SmallIntegerField(verbose_name="Value's weightage")

    objects = models.Manager()

    class Meta:
        """Table for assets"""
        db_table = "rating_values"


class Communities(models.Model):
    """
    Communities ORM model.

    Attributes:
        geo_id (int): ID
        name (string): Community name
        class_code (string): Class code
        latitude (double): Community's latitude
        longitude (double): Community's longitude
        objects(objects): Collection of objects. Part of Django.
    """
    geo_id = models.AutoField(primary_key=True, verbose_name="Geo ID")
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name="Community name")
    class_code = models.CharField(
        max_length=20,
        verbose_name="Community class code")
    latitude = models.DecimalField(
        null=False, verbose_name="Community's latitude")
    longitude = models.DecimalField(
        null=False, verbose_name="Community's longitude")

    objects = models.Manager()

    class Meta:
        """Table for assets"""
        db_table = "communities"


class Sources(models.Model):
    """
    Source ORM model.

    Attributes:
        type (int): Source type
        name (string): Source name
        objects(objects): Collection of objects. Part of Django.
    """
    type = models.AutoField(primary_key=True, verbose_name="Source type")
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name="Source name")

    objects = models.Manager()

    class Meta:
        """Table for assets"""
        db_table = "sources"


class Asset(models.Model):
    """
    Asset ORM model.

    Attributes:
        id (bigint): Asset ID
        name (string): Name of the asset.
        type (smallint): Asset type - 0:Tangible or 1:Intangible
        com_name (string): Community name
        com_geo_id (string): Community geo ID
        source_type (int): Source type
        source_name (string): Source name
        user_id (bigint): User's ID
        category (string): Category
        category_id (int): Category's ID
        description (string): Asset's description
        website (string): Asset's website - if applicable
        latitude (double): Asset's latitude
        longitude (double): Asset's longitude
        address (string): Asset's address
        timestamp (datetime): Create/update timestamp in UTC
        status (int): 0 - exists, 1 - missed, 2 - suggested

        objects(objects): Collection of objects. Part of Django.
    """
    TYPE_CHOICES = [
        (0, 'Tangible'),
        (1, 'Intangible'),
    ]
    STATUS_CHOICES = [
        (0, 'Status 0'),
        (1, 'Status 1'),
        (2, 'Status 2'),
    ]
    id = models.BigAutoField(primary_key=True, verbose_name="Asset ID")
    name = models.CharField(max_length=255, verbose_name="Asset's name")
    type = models.SmallIntegerField(
        choices=TYPE_CHOICES,
        verbose_name="Asset type - 0:Tangible or 1:Intangible")
    com_name = models.CharField(
        max_length=255,
        null=False,
        verbose_name="Community name")
    com_geo_id = models.IntegerField(
        null=False, verbose_name="Community geo ID")
    source_type = models.IntegerField(
        null=False, verbose_name="Asset's source type")
    source_name = models.CharField(max_length=255, verbose_name="Source name")
    user_id = models.BigIntegerField(verbose_name="User's ID")
    category = models.CharField(
        max_length=255,
        null=False,
        verbose_name="Asset's category")
    category_id = models.IntegerField(
        null=False, verbose_name="Category ID")
    description = models.TextField(verbose_name="Asset's description")
    website = models.TextField(verbose_name="Website")
    latitude = models.DecimalField(null=False, verbose_name="Asset's latitude")
    longitude = models.DecimalField(
        null=False, verbose_name="Asset's longitude")
    address = models.TextField(verbose_name="Asset's address")
    timestamp = models.DateTimeField(
        null=False, verbose_name="Timestamp in UTC")
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name="Asset's status: 0 - exists, 1 - missed, 2 - suggested")

    objects = models.Manager()

    # def __str__(self):
    #     return str(self.name)

    class Meta:
        """Table for assets"""
        db_table = "assets"


class AssetUpdates(models.Model):
    """
    AssetUpdates ORM model.

    Attributes:
        id (bigint): Update ID
        asset_id (bigint): Asset's ID
        name (string): Name of the asset.
        com_geo_id (string): Community geo ID
        category (string): Category
        category_id (int): Category's ID
        description (string): Asset's description
        website (string): Asset's website - if applicable
        latitude (double): Asset's latitude
        longitude (double): Asset's longitude
        address (string): Asset's address
        timestamp (datetime): Create/update timestamp in UTC
        type (smallint): 0 - Modify, 1 - Delete
        status (smallint):
            1 - Under review
            2 - Accepted
            3 - Rejected
            4 - Permanently closed
            5 - Temporarily closed
            6 - Never existed
            7 - None

        objects(objects): Collection of objects. Part of Django.
    """
    TYPE_CHOICES = [
        (0, 'Modify'),
        (1, 'Delete'),
    ]
    STATUS_CHOICES = [
        (1, 'Under Review'),
        (2, 'Accepted'),
        (3, 'Rejected'),
        (4, 'Permanently closed'),
        (5, 'Temporarily closed'),
        (6, 'Never existed'),
        (7, 'None'),
    ]
    id = models.BigAutoField(primary_key=True, verbose_name="Update ID")
    asset_id = models.BigAutoField(null=False, verbose_name="Asset ID")
    name = models.CharField(max_length=255, verbose_name="Asset's name")
    com_geo_id = models.IntegerField(
        null=False, verbose_name="Community geo ID")
    category = models.CharField(
        max_length=255,
        verbose_name="Category")
    category_id = models.IntegerField(verbose_name="Category ID")
    description = models.TextField(verbose_name="Description")
    website = models.TextField(verbose_name="Website")
    latitude = models.DecimalField(verbose_name="New latitude")
    longitude = models.DecimalField(verbose_name="New longitude")
    address = models.TextField(verbose_name="New address")
    timestamp = models.DateTimeField(
        null=False, verbose_name="Timestamp in UTC")
    type = models.SmallIntegerField(
        null=False,
        choices=TYPE_CHOICES,
        verbose_name="0 - Modify, 1 - Delete")
    status = models.IntegerField(
        null=False,
        choices=STATUS_CHOICES,
        default=0,
        verbose_name="1-Under review; \
            2-Accepted; \
            3-Rejected; \
            4-Permanently closed; \
            5-Temporarily closed; \
            6-Never existed; \
            7-None")

    objects = models.Manager()

    # def __str__(self):
    #     return str(self.name)

    class Meta:
        """Table for assets"""
        db_table = "asset_updates"


class AssetRatings(models.Model):
    """
    AssetRatings ORM model.

    Attributes:
        id (bigint): Rating ID
        asset_id (bigint): Asset's ID
        com_geo_id (string): Community geo ID
        user_id (bigint): User's ID
        timestamp (datetime): Create/update timestamp in UTC
        rating_scale (smallint): Rating scale
        comment (string): Comments
        value_id (smallint): Value ID

        objects(objects): Collection of objects. Part of Django.
    """
    id = models.BigAutoField(primary_key=True, verbose_name="Update ID")
    asset_id = models.BigAutoField(null=False, verbose_name="Asset ID")
    com_geo_id = models.IntegerField(
        null=False, verbose_name="Community geo ID")
    user_id = models.BigIntegerField(verbose_name="User ID")
    timestamp = models.DateTimeField(
        null=False, verbose_name="Timestamp in UTC")
    rating_scale = models.SmallIntegerField(verbose_name="Rating scale")
    comment = models.TextField(verbose_name="Comment")
    value_id = models.SmallIntegerField(verbose_name="Value ID")

    objects = models.Manager()

    # def __str__(self):
    #     return str(self.name)

    class Meta:
        """Table for assets"""
        db_table = "asset_ratings"
