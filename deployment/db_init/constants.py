"""
This file contains common constants utilized across multiple files.

Author: Niranjan Kumawat
"""
import os
import json

ROOT_PATH = f"{os.getcwd()}/deployment/db_init"

# Fetch the configuration file
CONFIGURATION = None
with open(f"{ROOT_PATH}/config.json", "r", encoding='utf-8') as cf:
    CONFIGURATION = json.load(cf)

# Environment Variables
DB_CONN_STRING = os.getenv("DB_CONN_STRING")
GOOGLE_API_KEY = os.getenv("G_API_KEY")

# DB tables
# Master tables
COMMUNITIES_TABLE = "communities"
ASSET_CATEGORIES_TABLE = "asset_categories"
SOURCES_TABLE = "sources"
RATING_VALUES_TABLE = "rating_values"
# Other table
ASSETS_TABLE = "assets"


# Fields
CATEGORY_FIELD = "category"
SOURCE_TYPE_FIELD = "source_type"
COMMUNITY_GEO_ID_FIELD = "community_geo_id"

# Response status
OK_STATUS = "OK"
REQUEST_DENIED_STATUS = "REQUEST_DENIED"

# Values
# Asset related
TANGIBLE_ASSET = 0 # Asset type - 0:Tangible or 1:Intangible

# Locations
ASSETS_DATA_LOC = "./data/assets.tsv"
ASSET_CATEGORIES_LOC = "./data/asset_categories.tsv"
COMMUNITIES_LOC = "./data/communities.tsv"
RATING_VALUES_LOC = "./data/rating_values.tsv"
SOURCES_LOC = "./data/sources.tsv"

# Google APIs
GOOGLE_APIS = CONFIGURATION["googleAPIs"]
GOOGLE_API_GEOCODE = GOOGLE_APIS["geocode"]
GOOGLE_API_PLACE_DETAILS = GOOGLE_APIS["placeDetails"]
GOOGLE_API_PLACE_NEARBY_SEARCH = GOOGLE_APIS["placeNearbySearch"]

# Hospital API
HOSPITAL_API = CONFIGURATION["hospitalAPI"]
