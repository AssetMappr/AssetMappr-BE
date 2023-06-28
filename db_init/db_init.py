"""
Initializes database and populate data.

Author: Mihir Bhaskar, Niranjan Kumawat
"""

import pandas as pd

from constants import DB_CONN_STRING, ASSET_CATEGORIES_LOC, \
    ASSET_CATEGORIES_TABLE, RATING_VALUES_LOC, RATING_VALUES_TABLE, \
    COMMUNITIES_TABLE, COMMUNITIES_LOC, SOURCES_LOC, SOURCES_TABLE, \
    ASSETS_DATA_LOC, ASSETS_TABLE
from db_utils import check_connection, drop_table, execute_queries, insert_into, \
    read_all_rows


ASSET_CATEGORIES_MAP = {}
SOURCES_MAP = {}


def drop_and_create():
    """
      Drops existing tables:
        1. asset_categories
        2. rating_values
        3. communities
        4. sources
        5. users
        6. profile
        7. assets
        8. asset_updates
        9. asset_ratings
        10. completed_surveys
        11. user_surveys

        and create same new ones.
    """
    # Drop all existing tables
    tables = [
        "asset_categories",
        "rating_values",
        "communities",
        "sources",
        "users",
        "profile",
        "assets",
        "asset_updates",
        "asset_ratings",
        "completed_surveys",
        "user_surveys"
    ]
    drop_table(tables)

    # Create new tables
    queries = []
    # Base tables
    # Asset Categories
    queries.append("CREATE TABLE asset_categories ("
                   "id SERIAL PRIMARY KEY NOT NULL,"
                   "category VARCHAR(255) NOT NULL,"
                   "description TEXT NOT NULL"
                   ");")
    # Rating Values
    queries.append("CREATE TABLE rating_values ("
                   "id SERIAL PRIMARY KEY NOT NULL,"
                   "value VARCHAR(255) NOT NULL,"
                   "weight SMALLINT NOT NULL"
                   ");")
    # Communities
    queries.append("CREATE TABLE communities ("
                   "geo_id INT PRIMARY KEY NOT NULL,"
                   "name VARCHAR(255) NOT NULL,"
                   "class_code VARCHAR(10),"
                   "latitude DOUBLE PRECISION NOT NULL,"
                   "longitude DOUBLE PRECISION NOT NULL"
                   ");")
    # Sources
    queries.append("CREATE TABLE sources ("
                   "type SERIAL PRIMARY KEY NOT NULL,"
                   "name VARCHAR(255) NOT NULL"
                   ");")

    # Users
    queries.append("CREATE TABLE users ("
                   "id BIGSERIAL PRIMARY KEY NOT NULL,"
                   "email VARCHAR(255) NOT NULL,"
                   "salt VARCHAR(16) NOT NULL,"
                   "passhash VARCHAR(100) NOT NULL"
                   ");")
    # Profile
    queries.append("CREATE TABLE profile ("
                   "u_id BIGINT NOT NULL,"
                   "type VARCHAR(25) NOT NULL,"
                   "first_name VARCHAR(255) NOT NULL,"
                   "last_name VARCHAR(255),"
                   "mobile VARCHAR(12),"
                   "com_name VARCHAR(255),"
                   "com_geo_id INT NOT NULL,"
                   "dob DATE NOT NULL,"
                   "ethnicity VARCHAR(100),"
                   "race VARCHAR(50),"
                   "gender VARCHAR(50),"
                   "PRIMARY KEY (u_id),"
                   "FOREIGN KEY (u_id) REFERENCES users (id),"
                   "FOREIGN KEY (com_geo_id) REFERENCES communities (geo_id)"
                   ");")
    # Assets
    queries.append(
        "CREATE TABLE assets ("
        "id BIGSERIAL PRIMARY KEY NOT NULL,"
        "name VARCHAR(255) NOT NULL,"
        "type VARCHAR(15) CHECK(type IN ('Tangible', 'Intangible')),"
        "com_name VARCHAR(255) NOT NULL,"
        "com_geo_id INT NOT NULL,"
        "source_type INT NOT NULL,"
        "source_name VARCHAR(255),"
        "user_id BIGINT,"
        "category VARCHAR(255) NOT NULL,"
        "category_id INT NOT NULL,"
        "description TEXT,"
        "website TEXT,"
        "latitude DOUBLE PRECISION NOT NULL,"
        "longitude DOUBLE PRECISION NOT NULL,"
        "address TEXT,"
        "timestamp TIMESTAMPTZ NOT NULL,"
        "status INT CHECK(status IN (0, 1, 2)),"
        "FOREIGN KEY (com_geo_id) REFERENCES communities (geo_id),"
        "FOREIGN KEY (category_id) REFERENCES asset_categories (id),"
        "FOREIGN KEY (source_type) REFERENCES sources (type),"
        "FOREIGN KEY (user_id) REFERENCES users (id)"
        ");")
    # Asset updates
    queries.append("CREATE TABLE asset_updates ("
                   "id BIGSERIAL PRIMARY KEY NOT NULL,"
                   "asset_id BIGINT NOT NULL,"
                   "com_geo_id INT NOT NULL,"
                   "name VARCHAR(255),"
                   "description TEXT,"
                   "address TEXT,"
                   "latitude DOUBLE PRECISION,"
                   "longitude DOUBLE PRECISION,"
                   "timestamp TIMESTAMPTZ NOT NULL,"
                   "category VARCHAR(255),"
                   "category_id INT,"
                   "type INT NOT NULL CHECK(type IN (0, 1)),"
                   "status INT NOT NULL,"
                   "FOREIGN KEY (asset_id) REFERENCES assets (id),"
                   "FOREIGN KEY (com_geo_id) REFERENCES communities (geo_id)"
                   ");")
    # Asset ratings
    queries.append("CREATE TABLE asset_ratings ("
                   "id BIGSERIAL PRIMARY KEY NOT NULL,"
                   "asset_id BIGINT NOT NULL,"
                   "com_geo_id INT NOT NULL,"
                   "user_id BIGINT NOT NULL,"
                   "timestamp TIMESTAMPTZ NOT NULL,"
                   "rating_scale SMALLINT NOT NULL,"
                   "comments TEXT,"
                   "value VARCHAR(255) NOT NULL,"
                   "FOREIGN KEY (asset_id) REFERENCES assets (id),"
                   "FOREIGN KEY (com_geo_id) REFERENCES communities (geo_id),"
                   "FOREIGN KEY (user_id) REFERENCES users (id)"
                   ");")
    # Completed surveys
    queries.append("CREATE TABLE completed_surveys ("
                   "survey_id BIGINT NOT NULL,"
                   "planner_id BIGINT NOT NULL,"
                   "survey_name TEXT NOT NULL,"
                   "survey_purpose TEXT NOT NULL,"
                   "s_time TIMESTAMPTZ NOT NULL,"
                   "e_time TIMESTAMPTZ NOT NULL,"
                   "com_name VARCHAR(255) NOT NULL,"
                   "report JSON NOT NULL,"
                   "report_link TEXT,"
                   "responses_count INT NOT NULL,"
                   "visibility INT NOT NULL DEFAULT 0,"
                   "PRIMARY KEY (survey_id, planner_id)"
                   ");")
    # User surveys -- past surveys
    queries.append("CREATE TABLE user_surveys ("
                   "survey_id BIGINT NOT NULL,"
                   "user_id BIGINT NOT NULL,"
                   "status INT NOT NULL DEFAULT 0,"
                   "PRIMARY KEY (survey_id, user_id)"
                   ");")

    execute_queries(queries)


def populate_base():
    """
      Populates the base tables:
      1. asset_categories
      2. rating_values
      3. communities
      4. sources

      Data source: './data/*'
    """
    # Asset Categories - id(auto) | category | description
    data = pd.read_csv(ASSET_CATEGORIES_LOC, sep='\t', header=0)
    columns = ["category", "description"]
    insert_into(ASSET_CATEGORIES_TABLE, columns, data)

    # Rating Values - id(auto) | value | weight
    data = pd.read_csv(RATING_VALUES_LOC, sep='\t', header=0)
    columns = ["value", "weight"]
    insert_into(RATING_VALUES_TABLE, columns, data)

    # Communities - geo_id | name | class_code | latitude | longitude
    data = pd.read_csv(COMMUNITIES_LOC, sep='\t', header=0)
    columns = ["geo_id", "name", "class_code", "latitude", "longitude"]
    insert_into(COMMUNITIES_TABLE, columns, data)

    # Sources - type(auto) | name
    data = pd.read_csv(SOURCES_LOC, sep='\t', header=0)
    columns = ["name"]
    insert_into(SOURCES_TABLE, columns, data)


def populate_assets():
    """
      Populates the asset information at loc './data/assets.tsv'
    """
    # Assets - name | type | com_name | com_geo_id | source_type | source_name |
    # user_id | category | category_id | description | website | latitude |
    # longitude | address | timestamp | status
    data = pd.read_csv(ASSETS_DATA_LOC, sep='\t', header=0)
    # Drop rows if source not part of base tables
    data = data[data["source_name"].isin(SOURCES_MAP.keys())]
    data["source_type"] = data["source_name"].map(SOURCES_MAP)

    # Drop rows if category not part of base tables
    data = data[data["category"].isin(ASSET_CATEGORIES_MAP.keys())]
    data["category_id"] = data["category"].map(ASSET_CATEGORIES_MAP)
    data.reset_index(drop=True, inplace=True)

    columns = data.columns.tolist()
    insert_into(ASSETS_TABLE, columns, data)


def create_map():
    """
      Creates map for categories
    """
    # Create categories map
    rows = read_all_rows("asset_categories")
    for row in rows:
        ASSET_CATEGORIES_MAP[row[1]] = row[0]

    # Create sources map
    rows = read_all_rows("sources")
    for row in rows:
        SOURCES_MAP[row[1]] = row[0]


def populate_data():
    # Operations
    # Add base/master tables
    populate_base()
    create_map()

    #  Add assets information
    populate_assets()


if __name__ == "__main__":
    # Check if connection string is set or not
    if not DB_CONN_STRING:
        print("Environment variable 'DB_CONN_STRING' not set")
        print("URI Format: dbname=<db_name> user=<user> host=<host> "
              "password=<secret>")
        exit()
    # Check connection
    if not check_connection(DB_CONN_STRING):
        print("Problem establishing a connection with database! Exiting")
        exit()

    # Drop and create new tables
    drop_and_create()
    # Populate base/master tables and assets' data
    populate_data()
