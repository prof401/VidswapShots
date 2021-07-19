import get_single_file_shots as gs
import point_map as pm

#shot_list = gs.file_shot_data("VidSwap-Data-Export-Playlist.json")
#shot_list = gs.file_shot_data("VidSwap-Data-Export-Playlist-464721.json")
shot_list = gs.file_shot_data("VidSwap-edges.json")

for shot in shot_list:
    print(shot)

pm.show_shots(shot_list)
