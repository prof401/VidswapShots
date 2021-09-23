import json

import requests
from psycopg2 import Error

import cloud_db_service as db
import vidswap_services as vs

print(">store_vidswap")
with requests.Session() as session:
    # login
    vs.login(session)

    # get all season
    season_list = vs.get_seasons(session)

    conn = None
    try:
        conn = db.get_connection()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)

    # get all games for those seasons
    print("start vidswap")
    for season in season_list:
        cursor = conn.cursor()
        if season[0] == "2020":
            for game in vs.get_season_schedule(session, season):
                game_json = vs.get_game_json(session, game['id'])
                db.insert_game(cursor, season[0], game_json)
        conn.commit()

    cursor.execute("SELECT * from games")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0], row[1], row[2], row[3], row[4], row[5])

    cursor.close()
    if conn is not None:
        conn.close()
print("<store_vidswap")
