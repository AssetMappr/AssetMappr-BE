"""
This file consists of utility methods used across db
operations

Author: Niranjan Kumawat
"""
import constants as const
import psycopg2
import psycopg2.extras as extras


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
    cursor.execute(f"SELECT * FROM {const.COMMUNITIES_MASTER_TABLE}")
    communities_ms = {tup[0] for tup in list(cursor.fetchall())}  # set

    # What categories are in the master table now?
    cursor.execute(f"SELECT * FROM {const.CATEGORIES_MASTER_TABLE}")
    categories_ms = {tup[0] for tup in list(cursor.fetchall())}  # set

    # What sources are in the master table now?
    cursor.execute(f"SELECT * FROM {const.SOURCES_MASTER_TABLE}")
    sources_ms = {tup[0] for tup in list(cursor.fetchall())}  # set

    # Get unique categories in incoming data
    unique_cats = set(data[const.CATEGORY_FIELD])
    diff_cats = unique_cats.difference(categories_ms)

    # Get unique sources in incoming data
    unique_sources = set(data[const.SOURCE_TYPE_FIELD])
    diff_sources = unique_sources.difference(sources_ms)

    # Get unique communities in incoming data
    unique_community = set(data[const.COMMUNITY_GEO_ID_FIELD])
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


def execute_values(conn, data_frame, table):
    """
    Inserts values in data to db in bulk.
    Source:
    https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/

    Parameters:
        conn: a psychopg2 database connection
        data(DataFrame): Data in dataframe
        table(str): The table where vallues are to be committed.
    """

    # Using psycopg2.extras.execute_values() to insert the dataframe

    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in data_frame.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(data_frame.columns))
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
