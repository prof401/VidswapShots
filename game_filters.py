import pandas as pd

import vidswap_field as vf


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


def shots_dataframe(data):
    shot_dict_list = []

    for tag_event in data['tagEvents']:
        if tag_event['tagResource']['name'] == 'Shot':
            shot_dict = {}
            for tag_key in tag_event.keys():
                if tag_key == 'tagResource':
                    pass
                elif tag_key == 'tagAttributes':
                    for tag_attr in tag_event['tagAttributes']:
                        if tag_attr['name'] == 'Net Location':
                            for net_key in tag_attr['value'].keys():
                                shot_dict['net_' + net_key] = tag_attr['value'][net_key]
                        elif tag_attr['name'] == 'Field Location':
                            for field_key in tag_attr['value'].keys():
                                shot_dict['fl_' + field_key] = tag_attr['value'][field_key]
                        else:
                            shot_dict[tag_attr['name']] = tag_attr['value']
                else:
                    shot_dict[tag_key] = tag_event[tag_key]
            shot_dict_list.append(shot_dict)
    df = pd.DataFrame(shot_dict_list)

    df['fl_x'] = ((df['fl_x'] - vf.x_int) / vf.x_slope)
    df['fl_y'] = (((df['fl_y'] - vf.y_int) / vf.y_slope) + vf.y_len)
    return df
