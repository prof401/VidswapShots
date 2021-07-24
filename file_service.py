import json


def get_game_json(file_name) -> list:
    with open(file_name) as json_file:
        game_data = json.load(json_file)
        return game_data
