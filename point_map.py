import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch

x_min = 0
x_max = 1024
x_left = 144.8
x_right = 885.2
y_min = -1.357040646
y_max = 887.2428977
y_top = 642.842879

x_yard = (x_right - x_left) / 44
x_width = (x_max - x_min) / x_yard
x_slope = (x_max - x_min) / x_width
x_int = x_min

y_yard = (y_max - y_top) / 18
y_len = (y_max - y_min) / y_yard
y_slope = (y_max - y_min) / y_len
y_int = y_min

y2m = 36 * 2.54 / 100  # mplsoccer plots everything in meters, will need to convert


def map_shots(shot_data):
    pitch = VerticalPitch(pitch_color='black', line_color='white', half=True,
                          pitch_type="custom", pitch_width=x_width * y2m, pitch_length=y_len * 2 * y2m,
                          goal_type='box', constrained_layout=True,
                          tight_layout=True)  # , line_zorder=2,  line_alpha=0.6)
    fig, ax = pitch.draw()

    for shot in shot_data:
        if 'Field Location' in shot:
            x_plot = (((shot['Field Location']['x'] - x_int) / x_slope)) * y2m
            y_plot = (((shot['Field Location']['y'] - y_int) / y_slope) + y_len) * y2m
            if 'Result' in shot:
                result = shot['Result']
            else:
                result = ''
            if result == 'goal':
                ax.plot(x_plot, y_plot, 'r.')
            elif result == 'save':
                ax.plot(x_plot, y_plot, 'y.')
            elif result == 'wide':
                ax.plot(x_plot, y_plot, 'g.')
            elif result == 'blocked':
                ax.plot(x_plot, y_plot, 'c.')
            else:
                ax.plot(x_plot, y_plot, 'm.')

    plt.show()
