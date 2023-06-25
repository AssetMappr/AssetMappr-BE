"""
This file contains common constants utilized across multiple files.

Author: Niranjan Kumawat
"""
import os

# Environment Variables
DB_CONN_STRING = os.getenv("DB_CONN_STRING")
GOOGLE_API_KEY = os.getenv("G_API_KEY")

# DB tables
# Master tables
COMMUNITIES_TABLE = "communities"
ASSET_CATEGORIES_TABLE = "asset_categories"
SOURCES_TABLE = "sources"
RATING_VALUES_TABLE = "rating_values"


# Fields
CATEGORY_FIELD = "category"
SOURCE_TYPE_FIELD = "source_type"
COMMUNITY_GEO_ID_FIELD = "community_geo_id"

# Response status
OK_STATUS = "OK"
REQUEST_DENIED_STATUS = "REQUEST_DENIED"

# Values
# Asset related
TANGIBLE_ASSET = "Tangible"

# Locations
ASSETS_DATA_LOC = "./data/assets.csv"