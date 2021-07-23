def parse_shot_data(data):
    shots = []
    for tag_event in data['tagEvents']:
        if tag_event['tagResource']['name'] == 'Shot':
            result = ""
            field_x = -1
            field_y = -1
            net_x = -1
            net_y = -1
            team = ""
            for tag_attr in tag_event['tagAttributes']:
                if tag_attr['name'] == 'Result':
                    result = tag_attr['value']
                elif tag_attr['name'] == 'Net Location':
                    net_x = tag_attr['value']['x']
                    net_y = tag_attr['value']['y']
                elif tag_attr['name'] == 'Field Location':
                    field_x = tag_attr['value']['x']
                    field_y = tag_attr['value']['y']
                elif tag_attr['name'] == 'Team':
                    team = tag_attr['value']
            if field_x != -1 and field_y != -1 and net_x != -1 and net_y != -1:
                shot_dict = dict(result=result, field_x=field_x, field_y=field_y, net_x=net_x, net_y=net_y, team=team)
                shots.append(shot_dict)
    return shots
