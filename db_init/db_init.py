"""
Initializes database and populate data.

Author: Niranjan Kumawat
"""
from db_init.constants import DB_CONN_STRING
from db_init.db_utils import check_connection, drop_table, execute_queries


def drop_and_create():

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
        "asset_ratings"
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
                   "id SERIAL PRIMARY KEY NOT NULL"
                   "value VARCHAR(255) NOT NULL,"
                   "weight SMALLINT NOT NULL"
                   ");")
    # Communities
    queries.append("CREATE TABLE communities ("
                   "id BIGSERIAL PRIMARY KEY NOT NULL,"
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

    # User
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
                   "com_id BIGINT NOT NULL,"
                   "dob DATE NOT NULL,"
                   "ethnicity VARCHAR(100),"
                   "race VARCHAR(50),"
                   "gender VARCHAR(50),"
                   "PRIMARY KEY (u_id),"
                   "FOREIGN KEY (u_id) REFERENCES users (id),"
                   "FOREIGN KEY (com_id) REFERENCES communities (id)"
                   ");")
    # Assets
    queries.append(
        "CREATE TABLE assets ("
        "id BIGSERIAL PRIMARY KEY NOT NULL,"
        "name VARCHAR(255) NOT NULL,"
        "type VARCHAR(15) CHECK(type IN ('Tangible', 'Intangible')),"
        "com_name VARCHAR(255) NOT NULL,"
        "com_id BIGINT NOT NULL,"
        "source_type INT NOT NULL,"
        "source_name VARCHAR(255),"
        "category VARCHAR(255) NOT NULL,"
        "category_id INT NOT NULL,"
        "description TEXT,"
        "website TEXT,"
        "latitude DOUBLE PRECISION NOT NULL,"
        "longitude DOUBLE PRECISION NOT NULL,"
        "address TEXT,"
        "timestamp TIMESTAMPTZ NOT NULL,"
        "status INT CHECK(type IN (0, 1, 2))"
        "FOREIGN KEY (com_id) REFERENCES communities (id),"
        "FOREIGN KEY (category_id) REFERENCES asset_categories (id)"
        ");")
    # Asset updates
    queries.append("CREATE TABLE asset_updates ("
                   "id BIGSERIAL PRIMARY KEY NOT NULL,"
                   "asset_id BIGINT NOT NULL,"
                   "com_id BIGINT NOT NULL,"
                   "name VARCHAR(255),"
                   "description TEXT,"
                   "address TEXT,"
                   "latitude DOUBLE PRECISION,"
                   "longitude DOUBLE PRECISION,"
                   "timestamp TIMESTAMPTZ NOT NULL,"
                   "category VARCHAR(255),"
                   "category_id INT,"
                   "type INT NOT NULL CHECK(type IN (0, 1)),"
                   "status INT NOT NULL"
                   "FOREIGN KEY (asset_id) REFERENCES assets (id),"
                   "FOREIGN KEY (com_id) REFERENCES communities (id)"
                   ");")
    # Asset ratings
    queries.append("CREATE TABLE asset_ratings ("
                   "id BIGSERIAL PRIMARY KEY NOT NULL,"
                   "asset_id BIGINT NOT NULL,"
                   "com_id BIGINT NOT NULL,"
                   "user_id BIGINT NOT NULL,"
                   "timestamp TIMESTAMPTZ NOT NULL,"
                   "rating_scale SMALLINT NOT NULL,"
                   "comments TEXT,"
                   "value VARCHAR(255) NOT NULL,"
                   "FOREIGN KEY (asset_id) REFERENCES assets (id),"
                   "FOREIGN KEY (com_id) REFERENCES communities (id),"
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
                   "report_link TEXT"
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

def populate_data():
    # Operations
    # TODO Add base/master tables
    # TODO Add assets information
    pass


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
