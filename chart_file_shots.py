import file_service as gs
import game_filters
import point_map as pm

game_json = gs.get_game_json("VidSwap-Data-Export-Playlist.json")
shot_list = game_filters.filter_shots(game_json)
pm.map_shots(shot_list)

game_json = gs.get_game_json("VidSwap-edges.json")
shot_list = game_filters.filter_shots(game_json)
pm.map_shots(shot_list)

game_json = gs.get_game_json("VidSwap-Data-Export-Playlist-464721.json")
shot_list = game_filters.filter_shots(game_json)
pm.map_shots(shot_list)

# for shot in shot_list:
#     print(shot)
