"""
This file contains common constants utilized across multiple files.

Author: Niranjan Kumawat
"""
import os

# Environment Variables
DB_URI_ENV = "DB_URI"
GOOGLE_API_KEY = os.getenv("G_API_KEY")

# DB tables
COMMUNITIES_MASTER_TABLE = "communities"
CATEGORIES_MASTER_TABLE = "categories"
SOURCES_MASTER_TABLE = "sources"
VALUES_MASTER_TABLE = "values"


# Fields
CATEGORY_FIELD = "category"
SOURCE_TYPE_FIELD = "source_type"
COMMUNITY_GEO_ID_FIELD = "community_geo_id"

# Response status
OK_STATUS = "OK"
REQUEST_DENIED_STATUS = "REQUEST_DENIED"
