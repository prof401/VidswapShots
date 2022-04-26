import requests
from psycopg2 import Error

import pymongo

import vidswap_services as vs

print(">store_vidswap")
with requests.Session() as session:
    # login
    vs.login(session)

    # get all season
    season_list = vs.get_seasons(session)

    client = None
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)

    mydb = client["games"]
    mycol = mydb["conference"]

# get all games for those seasons
    print("start vidswap")
    for season in season_list:
        for game in vs.get_season_schedule(session, season):
            game_json = vs.get_game_json(session, game['id'])
            mycol.insert_one(game_json)

print("<store_vidswap")
