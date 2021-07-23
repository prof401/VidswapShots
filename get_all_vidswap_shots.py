import json

import requests

import point_map as pm
import shot_parser

url = 'https://app.vidswap.com/api'


def login(session):
    with open('account.txt') as f:
        file_data = [x.rstrip() for x in f]
    login_data = '{"username": "' + file_data[0] + '", "password": "' + file_data[1] + '"}'
    login_form = {'method': 'user.account.authenticate', 'data': login_data}
    login_resp = session.post(url, login_form)


def get_seasons(session):
    my_schedules = {'method': 'user.schedule.list'}
    resp = session.post(url, data=my_schedules)
    data = json.loads(resp.text)
    schedule = []
    for season in data['data']:
        season_data = season['season'], season['id']
        schedule.append(season_data)
    return schedule


def get_season_schedule(session, season):
    game_ids = []
    if (season[0] == '2020'):
        season_data = '{"scheduleId": ' + str(season[1]) + '}'
        my_schedule = {'method': 'user.schedule.list', 'data': season_data}
        resp = session.post(url, data=my_schedule)
        data = json.loads(resp.text)
        for game in data['data']:
            game_ids.append(game['id'])
        # print(data['data'][0].keys())
    return game_ids


def get_game(session, game_id):
    game_json_url = "https://app.vidswap.com/api?method=user.timeline.exportData"
    playlist_data = '{"playlistId": ' + str(game_id) + '}'
    my_data = {'data': playlist_data}
    response = session.post(game_json_url, data=my_data)
    response_json = json.loads(response.text)
    return response_json


with requests.Session() as session:
    login(session)
    season_list = get_seasons(session)
    all_games = []
    for season in season_list:
        for game in get_season_schedule(session, season):
            all_games.append(game)
    shot_list = []
    for game_id in all_games:
        game_json = get_game(session, game_id)
        for shot in shot_parser.parse_shot_data(game_json):
            shot_list.append(shot)

    print(len(shot_list))
    pm.show_shots(shot_list)
    print(all_games)
