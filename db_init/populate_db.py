"""
This file populates the Render PostGres database with pre-populated assets.
Additionally, it checks to see if master tables are inconsistent with incoming data
Finally, it provides a method for populating the master tables.

Author: Jameson Carter, Niranjan Kumawat
"""

import os
import pandas as pd
import psycopg2
import psycopg2.extras as extras

from constants import COMMUNITIES_MASTER_TABLE, CATEGORIES_MASTER_TABLE, SOURCES_MASTER_TABLE, VALUES_MASTER_TABLE, CATEGORY_FIELD, SOURCE_TYPE_FIELD, COMMUNITY_GEO_ID_FIELD


def check_master_tables(data, conn):
    """
    Checks if communities, source_type, and categories in data is present in
    the master tables. Returns true if included, otherwise false.

    Parameters:
        conn: a psychopg2 database connection
        data: the data generated through getUniontown.py

    Returns:
        Boolean True or False, delineating whether master tables are in good shape
        to handle incoming dataset.
    """

    cursor = conn.cursor()
    # What communities are in the master table now?
    communities_ms_query = f"SELECT * FROM {COMMUNITIES_MASTER_TABLE}"
    cursor.execute(communities_ms_query)
    communities_res = cursor.fetchall()

    communities_ms = set([tup[0] for tup in communities_res])

    # What categories are in the master table now?
    categories_ms_query = f"SELECT * FROM {CATEGORIES_MASTER_TABLE}"
    cursor.execute(categories_ms_query)
    categories_res = list(cursor.fetchall())
    categories_ms = set([tup[0] for tup in categories_res])

    # What sources are in the master table now?
    sources_ms_query = f"SELECT * FROM {SOURCES_MASTER_TABLE}"
    cursor.execute(sources_ms_query)
    sources_res = list(cursor.fetchall())
    sources_ms = set([tup[0] for tup in sources_res])

    # Get unique categories in incoming data
    unique_cats = set(data[CATEGORY_FIELD])
    diff_cats = unique_cats.difference(categories_ms)

    # Get unique sources in incoming data
    unique_sources = set(data[SOURCE_TYPE_FIELD])
    diff_sources = unique_sources.difference(sources_ms)

    # Get unique communities in incoming data
    unique_community = set(data[COMMUNITY_GEO_ID_FIELD])
    diff_community = unique_community.difference(communities_ms)

    # If these do not already exist in the category table, submit them!
    # If they do not, do not submit them. Master tables must contain all
    # categories
    print("These categories are in the master table:\n")
    print(categories_ms)

    print("\nThese sources are in the master table:\n")
    print(sources_ms)

    print("\nThese community GEOIDs are in the master table:\n")
    print(communities_ms)

    if len(diff_cats) > 0 or len(diff_sources) > 0 or len(diff_community) > 0:
        print("\nThese categories are in the data, but not in the master table:")
        for cat in diff_cats:
            print(cat)

        print("\nThese sources are in the data, but not in the master table:")
        for source in diff_sources:
            print(source)

        print("\nThese community GEOIDs are in the data, but not in the master table:")
        for community in diff_community:
            print(community)

        print('\nAny discrepancies above MUST BE RESOLVED before proceeding')
        cursor.close()
        return False

    print('No discrepancies found between master tables and incoming data')
    cursor.close()
    return True


def populate_master_tables(conn):
    """
    Populates the master table from initial set of communities, categories, sources, and values.

    Parameters:
        conn: a psychopg2 database connection
    """

    # Create the record that will be used to populate the community master file
    community_master = pd.read_csv(
        "./data/communities.tsv", sep='\t', header=0)

    # Create the record that will be used to populate the source master file
    source_master = pd.read_csv("./data/sources.tsv", sep='\t', header=0)

    # Create the record that will be used to populate the categories master
    # file
    category_master = pd.read_csv("./data/categories.tsv", sep='\t', header=0)

    # Create the record that will be used to populate the values master file
    values_master = pd.read_csv("./data/values.tsv", sep='\t', header=0)

    # categories_master
    execute_values(conn, category_master, CATEGORIES_MASTER_TABLE)

    # sources_master
    execute_values(conn, source_master, SOURCES_MASTER_TABLE)

    # communities_master
    execute_values(conn, community_master, COMMUNITIES_MASTER_TABLE)

    # values_master
    execute_values(conn, values_master, VALUES_MASTER_TABLE)


def execute_values(conn, df, table):
    """
    Inserts values in data to db in bulk.
    Source: https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/

    Parameters:
        conn: a psychopg2 database connection
        data(DataFrame): Data in dataframe
        table(str): The table where vallues are to be committed.
    """

    # Using psycopg2.extras.execute_values() to insert the dataframe

    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL quert to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return
    print(f"Values inserted into table: {table}")
    cursor.close()


def track_exists(cursor, asset_name, address, latitude, longitude):
    """
    Checks is an asset exists w/ given information

    Parameters:
        cursor: a psychopg2-initialized cursor with connection to our database
        asset_name(str): Asset's name
        address(str): Asset's address
        latitude(float): Asset's latitude
        longitude(float): Asset's longitude

    Returns:
        True if exists, otherwise false.
    """
    query = ("SELECT asset_name, address, latitude, longitude "
             "FROM assets WHERE asset_name = %s OR address = %s "
             "OR latitude = %s AND longitude = %s")

    vals = (asset_name, address, latitude, longitude)

    cursor.execute(query, vals)
    return cursor.fetchone() is not None


'''

'''


def populate_db(data, conn):
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
    '''
    potential_dupes = []
    for index, row in data.iterrows():
        result = track_exists(cursor, row['asset_name'],
                             row['address'],
                             row['latitude'],
                             row['longitude'])
        potential_dupes.append(result)
    print(potential_dupes)
    '''
    '''
    insert contingency
    '''
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
    con_string = os.getenv("DB_URI")

    # Establish connection with database
    conn = psycopg2.connect(con_string)
    data = pd.read_csv('/AssetMappr/database/NationalData.csv')
    populate_db(data, conn)
