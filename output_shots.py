import csv

import requests

import game_filters as gf
import vidswap_services as vs

with requests.Session() as session:
    vs.login(session)
    season_list = vs.get_seasons(session)
    all_games = []
    for season in season_list:
        for game in vs.get_season_schedule(session, season):
            all_games.append(game)
    shot_list = []
    print(len(all_games))
    for game in all_games:
        game_json = vs.get_game_json(session, game['id'])
        for shot in gf.filter_shots(game_json):
            shot_list.append(shot)

with open('shots.csv', 'w', newline='\n') as csvfile:
    fieldnames = ['Team', 'Result', 'f_x', 'f_y', 'f_sector']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for shot in shot_list:
        if 'Field Location' in shot:
            for key in shot['Field Location'].keys():
                shot['f_' + key] = shot['Field Location'][key]
        writer.writerow(shot)
