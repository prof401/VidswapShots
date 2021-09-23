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

    return connection


def print_db_info():
    connection = None
    try:
        connection = get_connection()
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
        if connection:
            connection.close()
            print("PostgreSQL connection is closed")


def setup_db():
    print(">setup_db")
    commands = (
        "DROP TABLE IF EXISTS teams CASCADE;",
        "CREATE TABLE teams ( "
        "   team_id SERIAL PRIMARY KEY, "
        "   team_name VARCHAR(255) NOT NULL "
        ");",
        "DROP TABLE IF EXISTS games CASCADE;",
        """ CREATE TABLE games (
                game_id SERIAL PRIMARY KEY,
                season SMALLINT NOT NULL,
                playlist_id SERIAL NOT NULL,
                playlist_name VARCHAR(255) NOT NULL,
                playlist_date TIMESTAMP,
                home_team_name VARCHAR(255) NOT NULL,
                away_team_name VARCHAR(255) NOT NULL
                );
        """,
        "DROP TABLE IF EXISTS events CASCADE;",
        """ CREATE TABLE events (
                event_id SERIAL PRIMARY KEY,
                game_id SERIAL,
                startOffset TIMESTAMP,
                endOffset TIMESTAMP,
                resource_name VARCHAR(255) NOT NULL,
                attrbutes JSON,
                CONSTRAINT fk_game
                    FOREIGN KEY(game_id) 
	                REFERENCES games(game_id)
                );
        """)
    conn = None
    try:
        conn = get_connection()
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
    print("<setup_db")


def test_db():
    insert_sql: str = "INSERT INTO teams (team_name) VALUES ( %s);"
    select_sql: str = "SELECT * from teams;"
    conn = None
    try:
        print('>test_db')
        conn = get_connection()
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
        print('<test_db')

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn is not None:
            conn.close()


def insert_game(cursor, season, game):
    insert_game_sql: str = "INSERT INTO games (" \
                           "season, " \
                           "playlist_id , " \
                           "playlist_name, " \
                           "playlist_date, " \
                           "home_team_name, " \
                           "away_team_name)" \
                           " VALUES (%s, %s, %s, %s, %s, %s);"
    # cursor.execute(insert_sql, season)
    data = [season, game['playlist']['id'], game['playlist']['name'], game['playlist']['date'],
            game['playlist']['homeTeam'], game['playlist']['awayTeam']]
    cursor.execute(insert_game_sql, data)
    insert_events(cursor, game['playlist']['id'], game['tagEvents'])


def insert_events(cursor, playlist_id, events):
    print(playlist_id)
    for event in events:
        print(event['tagResource']['name'])
        print(event['startOffset'])
        print(event['endOffset'])
        print(event['tagAttributes'])
        print()


def get_shots():
    select_sql: str = "select games.playlist_id, e->>'tagAttributes' shot from " \
                      "games, json_array_elements(games.events) e " \
                      "where home_team_name = 'College of Idaho' and e->'tagResource'->>'name' = 'Shot';"
    conn = None
    try:
        print('>get_shots')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(select_sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)

        cur.close()
        # commit the changes
        conn.commit()
        print('<get_shots')

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn is not None:
            conn.close()
