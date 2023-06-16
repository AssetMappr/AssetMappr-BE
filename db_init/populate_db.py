"""
This file populates the Render PostGres database with pre-populated assets.
Additionally, it checks to see if master tables are inconsistent with incoming data
Finally, it provides a method for populating the master tables.

Author: Jameson Carter, Niranjan Kumawat
"""

import argparse
import os
import pandas as pd
import psycopg2
import psycopg2.extras as extras
import constants as const

from db_util import execute_values


def populate_db(conn, data):
    """
    This must insert into assets. One essential question- what happens if we try to
    populate something into the table that already exists? How do we delineate between
    new assets and assets that represent the same location, especially after ratings
    are added? One way of doing this is to check lat == lat and lon == lon

    Then, we only insert the rows which are not duplicative. This means we do not overwrite
    existing assets, unless their lat/lon points change. Or unless two assets share
    the same location, which is possible... So maybe when lat/lon match I prompt
    the user and let them know, showing the asset currently in that location. If
    that asset is not problematic, insert. Otherwise exclude it. This way the uuids
    do not get overwritten, either.

    Parameters:
        data: the data generated through getUniontown.py
        conn: a psychopg2 database connection

    """
    extras.register_uuid()
    # What assets are in the master table now, for this community?
    # tuple format ex: [(4278528, 'Uniontown', 'C5', 39.8993024, -79.7245287)]
    #
    # potential_dupes = []
    # for index, row in data.iterrows():
    #     result = track_exists(cursor, row['asset_name'],
    #                          row['address'],
    #                          row['latitude'],
    #                          row['longitude'])
    #     potential_dupes.append(result)
    # print(potential_dupes)
    #
    #
    # insert contingency
    #
    categories = data[['asset_id', 'category']]
    data = data[['asset_id',
                 'asset_name',
                 'description',
                 'asset_type',
                 'community_geo_id',
                 'source_type',
                 'website',
                 'latitude',
                 'longitude',
                 'address',
                 'generated_timestamp']]

    # Drop exact duplicates in 'data' once we've removed the categories (if
    # multiple categories)
    data = data.drop_duplicates()

    execute_values(conn, data, 'assets')
    execute_values(conn, categories, 'asset_categories')


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "data_file",
        type=str,
        help="Path to data .csv file to be uploaded.")
    ARGS = PARSER.parse_args()

    DB_URI = os.getenv(const.DB_URI_ENV)

    if not DB_URI:
        print("Add the DB_URI in environment variables.")
    else:
        # Establish connection with database
        CONN = psycopg2.connect(DB_URI)
        DATA = pd.read_csv(ARGS.data_file)
        populate_db(CONN, DATA)
