#The basics
import pandas as pd
import numpy as np
import json

#Plotting
import matplotlib.pyplot as plt
from matplotlib import cm
from mplsoccer import VerticalPitch

shots_model = pd.read_json(r'/Users/prof401/IdeaProjects/xgdata.json')

H_Shot = np.histogram2d(shots_model['x'], shots_model['y'],bins=32,range=[[-32, 32],[0, 64]])
goals_only=shots_model[shots_model['goal']]
H_Goal=np.histogram2d(goals_only['x'], goals_only['y'],bins=32,range=[[-32, 32],[0, 64]])

pitch = VerticalPitch(pitch_color='black', line_color='black', half=True,
                      pitch_type="custom", pitch_width=64, pitch_length=128,
                      goal_type='box', constrained_layout=True,
                      tight_layout=True)

fig, ax = pitch.draw()
ax.imshow(H_Shot[0].T, extent=[0, 64, 64, 130], aspect='auto',cmap=plt.cm.Reds)
plt.show()

fig, ax = pitch.draw()
ax.imshow(H_Goal[0].T, extent=[0, 64, 64, 130], aspect='auto',cmap=plt.cm.Reds)
plt.show()

fig, ax = pitch.draw()
ax.imshow(H_Goal[0].T/H_Shot[0].T, extent=[0, 64, 64, 130], aspect='auto',cmap=plt.cm.Reds, vmin=0, vmax=0.5)
plt.show()
