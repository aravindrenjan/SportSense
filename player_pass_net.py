from statsbombpy import sb
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import seaborn as sns
import pandas as pd
import streamlit as st
from matplotlib.patches import Patch
import matplotlib as mpl

def display_player_pass_network(match_id, player_name):
    mpl.rcParams['font.family'] = 'sans-serif'
    events = sb.events(match_id)
    events_1 = events[['team', 'type', 'minute', 'location', 'pass_end_location', 'pass_outcome', 'player']]
    events_1 = events_1[events_1['player'] == player_name].reset_index()
    events_1 = events_1[events_1['type'].isin(['Pass'])]
    Loc = events_1['location']
    Loc = pd.DataFrame(Loc.to_list(), columns=['x', 'y'])
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='#c7d5cc', stripe=True)
    fig, ax = pitch.draw(figsize=(10, 6.5))
    #plt.gca().invert_yaxis()

    kde = sns.kdeplot(x=Loc['x'], y=Loc['y'], shade=True, thresh=0.05, alpha=0.5, levels=12, cmap='gnuplot')

    for i in range(len(events_1)):
        if events_1.pass_outcome[i] == 'Incomplete' or events_1.pass_outcome[i] == 'Unknown':
            plt.plot((events_1.location[i][0], events_1.pass_end_location[i][0]), (events_1.location[i][1], events_1.pass_end_location[i][1]), color='red')
            plt.scatter(events_1.location[i][0], events_1.location[i][1], color='red')
        elif events_1.pass_outcome[i] == 'Pass Offside':
            plt.plot((events_1.location[i][0], events_1.pass_end_location[i][0]), (events_1.location[i][1], events_1.pass_end_location[i][1]), color='blue')
            plt.scatter(events_1.location[i][0], events_1.location[i][1], color='blue')
        elif events_1.pass_outcome[i] == 'Out':
            plt.plot((events_1.location[i][0], events_1.pass_end_location[i][0]), (events_1.location[i][1], events_1.pass_end_location[i][1]), color='yellow')
            plt.scatter(events_1.location[i][0], events_1.location[i][1], color='yellow')
        else:
            plt.plot((events_1.location[i][0], events_1.pass_end_location[i][0]), (events_1.location[i][1], events_1.pass_end_location[i][1]), color='black')
            plt.scatter(events_1.location[i][0], events_1.location[i][1], color='black')
            
            
    # Create custom legend patches with colors
    legend_labels = ['Incomplete/Unknown Pass', 'Offside Pass', 'Out of Play', 'Successful Pass']
    legend_colors = ['red', 'blue', 'yellow', 'black']
    patches = [Patch(facecolor=color, edgecolor='w') for color in legend_colors]

    # Add legends with color identification
    ax.legend(patches, legend_labels, loc='upper right')
    # Display the plot in Streamlit
    st.pyplot(fig)






