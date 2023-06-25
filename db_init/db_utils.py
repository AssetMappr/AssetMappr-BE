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
        print(f"Error: {e} occurred when establishing a connection "
              f"using {conn_string}")
        return False


def execute_queries(queries: list):
    """
      Executes command without fetching rows/results.

      Parameters:
          queries(list): List of queries to be executed
    """
    # TODO Try catch
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

    # Operations
    # TODO Delete all existing tables
    # TODO Create new tables
    # TODO Add base/master tables
    # TODO Add assets information

