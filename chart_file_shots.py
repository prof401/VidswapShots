import file_service as gs
import point_map as pm
import shot_parser

game_json = gs.get_game_json("VidSwap-Data-Export-Playlist.json")
shot_list = shot_parser.parse_shot_data(game_json)
pm.show_shots(shot_list)

game_json = gs.get_game_json("VidSwap-edges.json")
shot_list = shot_parser.parse_shot_data(game_json)
pm.show_shots(shot_list)

game_json = gs.get_game_json("VidSwap-Data-Export-Playlist-464721.json")
shot_list = shot_parser.parse_shot_data(game_json)
pm.show_shots(shot_list)

for shot in shot_list:
    print(shot)
