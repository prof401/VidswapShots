import matplotlib.pyplot as plt

from mplsoccer import VerticalPitch


def show_shots(shot_data):
    pitch = VerticalPitch(pitch_color='black', line_color='white', half=True,
                          pitch_type="custom", pitch_width=62, pitch_length=120,
                          constrained_layout=True, tight_layout=False, goal_type='box',
                          axis=True, label=True)
    fig, ax = pitch.draw()
    plt.show()
    yd_to_m=0.9144
    x_slope=16.9
    x_int=-32.9
    y_slope=-13
    y_int=858.3571273

    x_array=[]
    y_array=[]
    for shot in shot_data:
        x_array.append((shot['field_x']-x_int)/x_slope*yd_to_m)
        y_array.append(120-((shot['field_y']-y_int)/y_slope*yd_to_m))
    pitch.scatter(x_array, y_array,ax)