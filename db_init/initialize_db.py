"""
This file creates the required table and adds pre-detrmined
records to some tables like supported communities to communities
table.

Author: Mihir Bhaskar, Niranjan Kumawat
"""

import argparse
import os
import pandas as pd
import psycopg2
import constants as const

from db_util import execute_values


def drop_tables(conn):
    # Create cursor object
    cursor = conn.cursor()

    # Dropping existing tables
    cursor.execute('''
                DROP TABLE IF EXISTS assets_preloaded CASCADE;
                DROP TABLE IF EXISTS sources_master CASCADE;
                DROP TABLE IF EXISTS categories_master CASCADE;
                DROP TABLE IF EXISTS values_master CASCADE;
                DROP TABLE IF EXISTS communities_master CASCADE;

                DROP TABLE IF EXISTS assets CASCADE;
                DROP TABLE IF EXISTS asset_categories CASCADE;
                DROP TABLE IF EXISTS ratings CASCADE;
                DROP TABLE IF EXISTS values CASCADE;
                DROP TABLE IF EXISTS missing_assets CASCADE;

                DROP TABLE IF EXISTS staged_assets CASCADE;
                DROP TABLE IF EXISTS staged_asset_categories CASCADE;
                DROP TABLE IF EXISTS staged_ratings CASCADE;
                DROP TABLE IF EXISTS staged_values CASCADE;
                    ''')


def create_tables(conn):
    cursor = conn.cursor()
    # Creating the database structure
    create_db = '''

    CREATE TABLE SOURCES_MASTER(
        source_type VARCHAR(100),

        PRIMARY KEY(source_type)

        );

    CREATE TABLE CATEGORIES_MASTER(
        category VARCHAR(200),
        description TEXT,

        PRIMARY KEY(category)

        );

    CREATE TABLE COMMUNITIES_MASTER(
        community_geo_id INT,

        community_name VARCHAR(200),

        community_class_code CHAR(2),

        latitude DOUBLE PRECISION,

        longitude DOUBLE PRECISION,

        PRIMARY KEY(community_geo_id)

        );

    CREATE TABLE VALUES_MASTER(
        value VARCHAR(200),
        value_type TEXT,

        PRIMARY KEY(value)
        );

    CREATE TABLE ASSETS(
        asset_id CHAR(36) NOT NULL,
        asset_name VARCHAR(250) NOT NULL,
        asset_type VARCHAR(12) CHECK(asset_type IN ('Tangible', 'Intangible')),
        community_geo_id INT NOT NULL,
        source_type VARCHAR(100) NOT NULL,
        description TEXT,
        website TEXT,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        address VARCHAR(250),
        user_upload_ip TEXT,
        generated_timestamp TIMESTAMP,

        PRIMARY KEY (asset_id),

        CONSTRAINT fk_asset_community
            FOREIGN KEY(community_geo_id)
                REFERENCES communities_master(community_geo_id),

        CONSTRAINT fk_asset_source
            FOREIGN KEY(source_type)
                REFERENCES sources_master(source_type)
        );

    CREATE TABLE ASSET_CATEGORIES(
        asset_id CHAR(36) NOT NULL,
        category VARCHAR(200) NOT NULL,

        PRIMARY KEY (asset_id, category),

        CONSTRAINT fk_assetcat_assetid
            FOREIGN KEY(asset_id)
                REFERENCES assets(asset_id),

        CONSTRAINT fk_assetcat_cat
            FOREIGN KEY(category)
                REFERENCES categories_master(category)

        );

    CREATE TABLE RATINGS(
        rating_id CHAR(36) NOT NULL,
        asset_id CHAR(36) NOT NULL,
        user_community INT NOT NULL,
        user_upload_ip TEXT,
        generated_timestamp TIMESTAMP,
        rating_scale INT,
        comments TEXT,

        PRIMARY KEY(rating_id),

        CONSTRAINT fk_ratings_assetid
            FOREIGN KEY(asset_id)
                REFERENCES assets(asset_id),

        CONSTRAINT fk_ratings_community
            FOREIGN KEY(user_community)
                REFERENCES communities_master(community_geo_id)

        );

    CREATE TABLE VALUES(
        rating_id CHAR(36) NOT NULL,
        value VARCHAR(200) NOT NULL,

        PRIMARY KEY(rating_id, value),

        CONSTRAINT fk_values_ratingid
            FOREIGN KEY(rating_id)
                REFERENCES ratings(rating_id),

        CONSTRAINT fk_values_value
            FOREIGN KEY(value)
                REFERENCES values_master(value)

        );

    CREATE TABLE STAGED_ASSETS(
        staged_asset_id CHAR(36) NOT NULL,
        asset_name VARCHAR(250) NOT NULL,
        asset_type VARCHAR(12) CHECK(asset_type IN ('Tangible', 'Intangible')),
        community_geo_id INT NOT NULL,
        source_type VARCHAR(100) NOT NULL,
        description TEXT,
        website TEXT,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        address VARCHAR(250),
        user_name VARCHAR(200),
        user_role VARCHAR(300),
        user_upload_ip TEXT,
        generated_timestamp TIMESTAMP,

        PRIMARY KEY(staged_asset_id),

        CONSTRAINT fk_stagedasset_community
            FOREIGN KEY(community_geo_id)
                REFERENCES communities_master(community_geo_id),

        CONSTRAINT fk_stagedasset_source
            FOREIGN KEY(source_type)
                REFERENCES sources_master(source_type)
        );

    CREATE TABLE STAGED_ASSET_CATEGORIES(
        staged_asset_id CHAR(36) NOT NULL,
        category VARCHAR(200) NOT NULL,

        PRIMARY KEY(staged_asset_id, category),

        CONSTRAINT fk_stagedassetcat_id
            FOREIGN KEY(staged_asset_id)
                REFERENCES staged_assets(staged_asset_id),

        CONSTRAINT fk_stagedassetcat_cat
            FOREIGN KEY(category)
                REFERENCES categories_master(category)

        );

    CREATE TABLE STAGED_RATINGS(
        staged_rating_id CHAR(36) NOT NULL,
        asset_id CHAR(36) NOT NULL,
        user_community INT NOT NULL,
        user_name VARCHAR(200),
        user_role VARCHAR(300),
        user_upload_ip TEXT,
        generated_timestamp TIMESTAMP,
        rating_scale INT,
        comments TEXT,
        asset_status VARCHAR(12) CHECK(asset_status IN ('Staged', 'Verified')),

        PRIMARY KEY(staged_rating_id),

        CONSTRAINT fk_stagedratings_community
            FOREIGN KEY(user_community)
                REFERENCES communities_master(community_geo_id)

        );

    CREATE TABLE STAGED_VALUES(
        staged_rating_id CHAR(36) NOT NULL,
        value VARCHAR(200) NOT NULL,

        PRIMARY KEY(staged_rating_id, value),

        CONSTRAINT fk_stagedvalues_rating
            FOREIGN KEY(staged_rating_id)
                REFERENCES staged_ratings(staged_rating_id),

        CONSTRAINT fk_stagedvalues_value
            FOREIGN KEY(value)
                REFERENCES values_master(value)

        );

    CREATE TABLE MISSING_ASSETS(
        suggestion_id CHAR(36) NOT NULL,
        user_community INT NOT NULL,
        user_name VARCHAR(200),
        user_role VARCHAR(300),
        user_upload_ip TEXT,
        generated_timestamp TIMESTAMP,
        missing_asset_name VARCHAR(250),
        description TEXT,
        primary_category VARCHAR(200) NOT NULL,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        address TEXT,
        justification TEXT,
        line LINE,
        polygon POLYGON,
        circle CIRCLE,

        PRIMARY KEY(suggestion_id),

        CONSTRAINT fk_missingasset_community
            FOREIGN KEY(user_community)
                REFERENCES communities_master(community_geo_id),

        CONSTRAINT fk_missingasset_cat
            FOREIGN KEY(primary_category)
                REFERENCES categories_master(category)

        );

    CREATE TABLE SUGGESTED_EDITS(
        edit_id CHAR(36) NOT NULL,
        asset_id CHAR(36) NOT NULL,
        suggested_asset_name VARCHAR(250),
        suggested_description TEXT,
        suggested_address TEXT,
        suggested_latitude DOUBLE PRECISION,
        suggested_longitude DOUBLE PRECISION,
        suggested_website TEXT,
        current_status VARCHAR(300),
        suggested_category VARCHAR(200),
        user_upload_ip TEXT,
        generated_timestamp TIMESTAMP,

        PRIMARY KEY(edit_id),

        CONSTRAINT fk_suggestededit_assetid
            FOREIGN KEY(asset_id)
                REFERENCES assets(asset_id),

        CONSTRAINT fk_suggestededit_cat
            FOREIGN KEY(suggested_category)
                REFERENCES categories_master(category)

        );

    '''

    # Execute the query
    cursor.execute(create_db)


def populate_master_tables(conn, file, table):
    """
    Populates the master table from initial set of communities, categories, sources, and values.

    Parameters:
        conn: a psychopg2 database connection
        file(str): Location of the master data
        table(str): Table name to populate the data.
    """

    master = pd.read_csv(file, sep='\t', header=0)
    execute_values(conn, master, table)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "dir",
        type=str,
        help="Path to master directory files to be uploaded. Default is './data'",
        default="./data")
    ARGS = PARSER.parse_args()
    DIR = ARGS.dir
    DB_URI = os.getenv(const.DB_URI_ENV)

    if not DB_URI:
        print("Add the DB_URI in environment variables.")
    else:
        # Establish connection with database
        CONN = psycopg2.connect(DB_URI)

        # Drop existing tables
        drop_tables(CONN)

        # Create tables
        create_tables(CONN)

        populate_master_tables(
            CONN,
            f"{DIR}/communities.tsv",
            const.COMMUNITIES_MASTER_TABLE)
        populate_master_tables(
            CONN,
            f"{DIR}/sources.tsv",
            const.SOURCES_MASTER_TABLE)
        populate_master_tables(
            CONN,
            f"{DIR}/categories.tsv",
            const.CATEGORIES_MASTER_TABLE)
        populate_master_tables(
            CONN,
            f"{DIR}/values.tsv",
            const.VALUES_MASTER_TABLE)

        CONN.commit()
        CONN.close()
