import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch


def map_shots(shot_data):
    pitch = VerticalPitch(pitch_color='black', line_color='white', half=True,
                          pitch_type="custom", pitch_width=56, pitch_length=120,
                          constrained_layout=True, tight_layout=False, goal_type='box',
                          axis=True, label=True)
    fig, ax = pitch.draw()

    x_slope = 1024 / 61
    x_int = 0
    y_slope = -13
    y_int = 874
    yd_to_m = 0.9144

    for shot in shot_data:
        print(shot)
        if 'Field Location' in shot:
            x_plot = ((shot['Field Location']['x'] - x_int) / x_slope * yd_to_m)
            y_plot = (120 - ((shot['Field Location']['y'] - y_int) / y_slope * yd_to_m))
            ax.plot(x_plot, y_plot, 'ro')
    plt.show()
