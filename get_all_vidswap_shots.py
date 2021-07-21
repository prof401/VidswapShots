import requests
import json

url = 'https://app.vidswap.com/api'


def login(session):
    with open('account.txt') as f:
        file_data = [x.rstrip() for x in f]
    login_data = '{"username": "' + file_data[0] + '", "password": "' + file_data[1] + '"}'
    login_form = {'method': 'user.account.authenticate', 'data': login_data}
    login_resp = session.post(url, login_form)


def get_schedules(session):
    my_schedules = {'method': 'user.schedule.list'}
    resp = sess.post(url, data=my_schedules)
    data = json.loads(resp.text)
    schedule = []
    for season in data['data']:
        season_data = season['season'], season['id']
        schedule.append(season_data)
    return schedule


def get_schedule(session, season):
    season_data = '{"scheduleId": ' + str(season[1]) + '}'
    my_schedule = {'method': 'user.schedule.list', 'data': season_data}
    resp = session.post(url, data=my_schedule)
    if (season[0]=='2020') :
        data = json.loads(resp.text)
        print(data['data'][0].keys())
        #print(resp.text)


sess = requests.session()
login(sess)
schedule_list = get_schedules(sess)
for season in schedule_list:
    get_schedule(sess, season)
