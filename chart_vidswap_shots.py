import pandas as pd
import requests

import game_filters as gf
import point_map as pm
import vidswap_services as vs

with requests.Session() as session:
    # login
    vs.login(session)

    # get all season
    season_list = vs.get_seasons(session)

    # get all games for those seasons
    all_games = []
    for season in season_list:
        if season[0] == "2020":
            for game in vs.get_season_schedule(session, season):
                game_json = vs.get_game_json(session, game['id'])
                shot_df = shot_df.append(gf.shots_dataframe(game_json))
                all_games.append(game)

    # get shots for all those games
    shot_df = pd.DataFrame(columns=['id'])
    for game in all_games:
        game_json = vs.get_game_json(session, game['id'])
        shot_df = shot_df.append(gf.shots_dataframe(game_json))

    # chart shots
    pm.chart_shots(shot_df)
