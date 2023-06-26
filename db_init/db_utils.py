"""
Wrapper functions to use the database.

Author: Niranjan Kumawat
"""
import psycopg2

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
    except psycopg2.OperationalError as e:
        print(f"Exception: {e} occurred when establishing a connection "
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
    except (psycopg2.OperationalError, psycopg2.DatabaseError) as e:
        print(f"Exception: {e}")


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
