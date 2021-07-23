import json

import shot_parser


def file_shot_data(file_name: object) -> list:
    with open(file_name) as json_file:
        game_data = json.load(json_file)
    shot_list = shot_parser.parse_shot_data(game_data)
    return shot_list
