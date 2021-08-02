import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch

import vidswap_field as vf

y2m = 36 * 2.54 / 100  # mplsoccer plots everything in meters, will need to convert


def map_shots(shot_data):
    pitch = VerticalPitch(pitch_color='black', line_color='white', half=True,
                          pitch_type="custom", pitch_width=vf.x_width * y2m, pitch_length=vf.y_len * 2 * y2m,
                          goal_type='box', constrained_layout=True,
                          tight_layout=True)  # , line_zorder=2,  line_alpha=0.6)
    fig, ax = pitch.draw()

    for shot in shot_data:
        if 'Field Location' in shot:
            x_plot = ((shot['Field Location']['x'] - vf.x_int) / vf.x_slope) * y2m
            y_plot = (((shot['Field Location']['y'] - vf.y_int) / vf.y_slope) + vf.y_len) * y2m
            if 'Result' in shot:
                result = shot['Result']
            else:
                result = ''
            if result == 'goal':
                ax.plot(x_plot, y_plot, 'r.', label='Goal')
            elif result == 'save':
                ax.plot(x_plot, y_plot, 'y.')
            elif result == 'wide':
                ax.plot(x_plot, y_plot, 'g.')
            elif result == 'blocked':
                ax.plot(x_plot, y_plot, 'c.')
            else:
                ax.plot(x_plot, y_plot, 'm.')
    plt.show()


def chart_shots(shot_df):
    pitch = VerticalPitch(pitch_color='black', line_color='white', half=True,
                          pitch_type="custom", pitch_width=vf.x_width * y2m, pitch_length=vf.y_len * 2 * y2m,
                          goal_type='box', constrained_layout=True,
                          tight_layout=True)
    fig, ax = pitch.draw()

    # ax.plot(shot_df['fl_x'] * y2m, shot_df['fl_y'] * y2m, 'r.')
    if 'Result' in shot_df:
        df_blocked = shot_df[shot_df.Result == 'blocked']
        ax.plot(df_blocked['fl_x'] * y2m, df_blocked['fl_y'] * y2m, 'c.', label='Blocked')
        df_wide = shot_df[shot_df.Result == 'wide']
        ax.plot(df_wide['fl_x'] * y2m, df_wide['fl_y'] * y2m, 'g.', label='Wide')
        df_save = shot_df[shot_df.Result == 'save']
        ax.plot(df_save['fl_x'] * y2m, df_save['fl_y'] * y2m, 'y.', label='Save')
        df_goal = shot_df[shot_df.Result == 'goal']
        ax.plot(df_goal['fl_x'] * y2m, df_goal['fl_y'] * y2m, 'r.', label='Goal')
    else:
        ax.plot(shot_df['fl_x'] * y2m, shot_df['fl_y'] * y2m, 'm.', label='Unknown')

    plt.legend(loc="lower right")
    plt.savefig('/Users/prof401/Documents/shots.svg')
    plt.show()
