"""
This file contains common constants utilized across multiple files.

Author: Niranjan Kumawat
"""
import os

# Environment Variables
DB_URI_ENV = "DB_URI"
GOOGLE_API_KEY = os.getenv("G_API_KEY")

# DB tables
COMMUNITIES_MASTER_TABLE = "communities_master"
CATEGORIES_MASTER_TABLE = "categories_master"
SOURCES_MASTER_TABLE = "sources_master"
VALUES_MASTER_TABLE = "values_master"


# Fields
CATEGORY_FIELD = "category"
SOURCE_TYPE_FIELD = "source_type"
COMMUNITY_GEO_ID_FIELD = "community_geo_id"