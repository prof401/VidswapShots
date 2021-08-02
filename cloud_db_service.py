import configparser

import psycopg2
from psycopg2 import Error


def get_connection():
    """
    Return a connection to the db.
    """
    config_obj = configparser.ConfigParser()
    config_obj.read("config.ini")
    cloud_config = config_obj["cloud_database"]
    message = ''

    try:
        connection = psycopg2.connect(
            host=cloud_config["host"],
            database=cloud_config["database"],
            user=cloud_config["user"],
            password=cloud_config["password"],
            sslcert=cloud_config["sslcert"],
            sslkey=cloud_config["sslkey"],
            sslrootcert=cloud_config["sslrootcert"],
            sslmode=cloud_config["sslmode"])

    except (Exception, Error) as error:
        return None, 'Error : Server cannot connect to database'

    return connection, message


def print_db_info():
    connection = None
    try:
        connection, msg = get_connection()
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        cursor.close()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            connection.close()
            print("PostgreSQL connection is closed")


def setup_db():
    commands = (
        " DROP TABLE IF EXISTS teams;",
        """
            CREATE TABLE teams (
                team_id SERIAL PRIMARY KEY,
                team_name VARCHAR(255) NOT NULL
            )
            """,
        """ DROP TABLE IF EXISTS games;
        """,
        """ CREATE TABLE games (
                game_id SERIAL PRIMARY KEY,
                playlist_id VARCHAR(255) NOT NULL,
                playlist_name VARCHAR(255) NOT NULL,
                playlist_date TIMESTAMP,
                home_team_name VARCHAR(255) NOT NULL,
                away_team_name VARCHAR(255) NOT NULL,
                event_id VARCHAR(255) NOT NULL,
                event_start_offset VARCHAR(255) NOT NULL,
                event_end_offset VARCHAR(255) NOT NULL,
                resource_id VARCHAR(255) NOT NULL,
                resource_name VARCHAR(255) NOT NULL,
                attributes JSON
                )
        """)
    conn = None
    try:
        conn, msg = get_connection()
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn is not None:
            conn.close()


def test_db():
    insert_sql: str = """INSERT INTO teams (team_name) VALUES ( %s);"""
    select_sql: str = """SELECT * from teams;"""
    conn = None
    try:
        conn, msg = get_connection()
        cur = conn.cursor()
        cur.execute(insert_sql, ["College of Idaho"])
        cur.execute(insert_sql, ["Carroll College"])
        cur.execute(insert_sql, ["Boise State"])

        cur.execute(select_sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)

        cur.close()
        # commit the changes
        conn.commit()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn is not None:
            conn.close()


# print_db_info()
setup_db()
test_db()
