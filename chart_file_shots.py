import file_service as gs
import game_filters
import point_map as pm

game_json = gs.get_game_json("VidSwap-Data-Export-Playlist.json")
df = game_filters.shots_dataframe(game_json)
pm.chart_shots(df)

game_json = gs.get_game_json("VidSwap-edges.json")
df = game_filters.shots_dataframe(game_json)
pm.chart_shots(df)

game_json = gs.get_game_json("VidSwap-Data-Export-Playlist-464721.json")
df = game_filters.shots_dataframe(game_json)
pm.chart_shots(df)
