import requests

import point_map as pm
import shot_parser
import vidswap_services as vs

with requests.Session() as session:
    vs.login(session)
    season_list = vs.get_seasons(session)
    all_games = []
    for season in season_list:
        for game in vs.get_season_schedule(session, season):
            all_games.append(game)
    shot_list = []
    for game_id in all_games:
        game_json = vs.get_game_json(session, game_id)
        for shot in shot_parser.parse_shot_data(game_json):
            shot_list.append(shot)

    print(len(shot_list))
    pm.show_shots(shot_list)
    print(all_games)
