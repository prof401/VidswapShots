import json

base_url = 'https://app.vidswap.com/api'
game_json_url = base_url + "?method=user.timeline.exportData"


def login(session):
    with open('account.txt') as f:
        file_data = [x.rstrip() for x in f]
    login_data = '{"username": "' + file_data[0] + '", "password": "' + file_data[1] + '"}'
    login_form = {'method': 'user.account.authenticate', 'data': login_data}
    login_resp = session.post(base_url, login_form)


def get_seasons(session) -> list:
    my_schedules = {'method': 'user.schedule.list'}
    resp = session.post(base_url, data=my_schedules)
    data = json.loads(resp.text)
    schedule = []
    for season in data['data']:
        season_data = season['season'], season['id']
        schedule.append(season_data)
    return schedule


def get_season_schedule(session, season) -> list:
    games = []
    season_data = '{"scheduleId": ' + str(season[1]) + '}'
    my_schedule = {'method': 'user.schedule.list', 'data': season_data}
    resp = session.post(base_url, data=my_schedule)
    data = json.loads(resp.text)
    for game in data['data']:
        games.append(game)
    # print(data['data'][0].keys())
    return games


def get_game_json(session, game_id) -> dict:
    playlist_data = '{"playlistId": ' + str(game_id) + '}'
    my_data = {'data': playlist_data}
    response = session.post(game_json_url, data=my_data)
    response_json = json.loads(response.text)
    return response_json
