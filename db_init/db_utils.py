"""
Wrapper functions to use the database.

Author: Niranjan Kumawat
"""
import psycopg2
from psycopg2 import extras
from pandas import DataFrame

from db_init.constants import DB_CONN_STRING


def check_connection(conn_string: str):
    """
      Checks postgreSQL database connection using connection string.

      Parameters:
          conn_string(str): 2 character state postal code

      Returns:
          True if connection established, otherwise false.
    """
    try:
        conn = psycopg2.connect(f"{conn_string} connect_timeout=1")
        conn.close()
        return True
    except psycopg2.OperationalError as exception:
        print(
            f"Exception: {exception} occurred when establishing a connection "
            f"using {conn_string}")
        return False


def execute_queries(queries: list):
    """
      Executes command without fetching rows/results.

      Parameters:
          queries(list): List of queries to be executed
    """
    try:
        # Establish a connection
        conn = psycopg2.connect(DB_CONN_STRING)
        # Open a cursor to perform database operations
        cur = conn.cursor()
        # Execute a command
        for query in queries:
            cur.execute(query)
        # Make the changes to the database persistent
        conn.commit()
        # Close cursor and communication with the database
        cur.close()
        # Close connection
        conn.close()
    except (psycopg2.OperationalError, psycopg2.DatabaseError) as exception:
        print(f"Exception: {exception}")


def drop_table(tables: list):
    """
      Drops a table, if exist, in the tables.

      Parameters:
          tables(list): List of tables to be deleted
    """
    queries = []
    for table in tables:
        queries.append(f"DROP TABLE IF EXISTS {table} CASCADE;")
    execute_queries(queries)


def insert_into(table: str, columns: list, data: DataFrame):
    """
      Inserts data into table

      Parameters:
          table(str): Table name
          columns(list): Columns for which values are to be added.
          data(DataFrame): Values corresponding to columns
    """
    columns = ",".join(columns)
    query = f"INSERT INTO {table}({columns}) VALUES %%s"
    tuples = [tuple(x) for x in data.to_numpy()]
    conn = psycopg2.connect(DB_CONN_STRING)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (psycopg2.OperationalError, psycopg2.DatabaseError) as exception:
        print(f"Exception occurred: {exception}")
        conn.rollback()
        cursor.close()
        return

    print(f"Inserted data to {table}")
    cursor.close()
    conn.close()


def read_all_rows(table: str):
    """
      Read all rows and columns for given table.

      Parameters:
          table(str): Table name
      Returns:
          Rows [(1, 100, "abcdef"), (2, None, 'dada')], otherwise None
    """
    conn = None
    rows = []
    try:
        # Establish a connection
        conn = psycopg2.connect(DB_CONN_STRING)
        # Open a cursor to perform database operations
        cur = conn.cursor()
        # Execute a command
        query = f"SELECT * FROM {table};"
        cur.execute(query)
        rows = cur.fetchall()
        # Close cursor and communication with the database
        cur.close()
    except (psycopg2.OperationalError, psycopg2.DatabaseError) as exception:
        print(f"Exception: {exception}")
    finally:
        if conn:
            # Close connection
            conn.close()
    return rows
