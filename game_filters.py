def filter_shots(data) -> list:
    shots = []
    for tag_event in data['tagEvents']:
        if tag_event['tagResource']['name'] == 'Shot':
            result = ""
            new_dict = {}
            for tag_attr in tag_event['tagAttributes']:
                new_dict[tag_attr['name']] = tag_attr['value']
            shots.append(new_dict)
    return shots
