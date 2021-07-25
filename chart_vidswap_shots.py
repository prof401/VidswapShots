import requests

import game_filters as gf
import point_map as pm
import vidswap_services as vs

with requests.Session() as session:
    vs.login(session)
    season_list = vs.get_seasons(session)
    all_games = []
    for season in season_list:
        if (season[0] == "2020"):
            for game in vs.get_season_schedule(session, season):
                    all_games.append(game)
    shot_list = []
    for game in all_games:
        game_json = vs.get_game_json(session, game['id'])
        for shot in gf.filter_shots(game_json):
            shot_list.append(shot)

    print(len(shot_list))
    pm.map_shots(shot_list)
    print(all_games)
