import streamlit as st
import pandas as pd
from mplsoccer import Pitch
from statsbombpy import sb
import matplotlib.pyplot as plt
import mpld3
import matplotlib as mpl

def prepare_shots_data(shots):
    mpl.rcParams['font.family'] = 'sans-serif'
    shots = shots[['team', 'player', 'minute', 'second', 'location', 'shot_statsbomb_xg', 'shot_outcome']]
    # shots['x'] = shots.location.apply(lambda x: x[0])
    # shots['y'] = shots.location.apply(lambda x: x[1])
    shots['x'] = shots.location.str[0].values
    shots['y'] = shots.location.str[1].values
    shots = shots.drop('location', axis=1)
    # Divide the dataset based on the outcome
    goals = shots[shots.shot_outcome == 'Goal']
    shots = shots[shots.shot_outcome != 'Goal']
    return shots, goals


def render_shots_chart(shots, home_team, away_team, home_score, away_score):
    # Filter shots by team (home_team and away_team)
    shots1 = shots[shots.team == home_team]
    shots2 = shots[shots.team == away_team]

    # Prepare shots data for plotting
    shots1, goals1 = prepare_shots_data(shots1)
    shots2, goals2 = prepare_shots_data(shots2)
    
    pitch = Pitch(pitch_type='statsbomb', half=False, goal_type='box', goal_alpha=0.8, pitch_color='grass', line_color='white', stripe=True)
    fig, axs = pitch.grid(figheight=8, title_height=0.08, endnote_space=0, axis=False, title_space=0, grid_height=0.72, endnote_height=0.05)
    fig.set_facecolor("#22312b")

    scatter_shots = pitch.scatter(shots1.x, shots1.y, s=(shots1.shot_statsbomb_xg * 900) + 100, c='#FE9694', edgecolors='#606060', marker='o', ax=axs['pitch'], hatch='///', label=home_team)
    scatter_goals = pitch.scatter(goals1.x, goals1.y, s=(goals1.shot_statsbomb_xg * 900) + 100, c='white', edgecolors='black', marker='football', ax=axs['pitch'])

    scatter_shots = pitch.scatter(120-(shots2.x), 80-(shots2.y), s=(shots2.shot_statsbomb_xg * 900) + 100, c='#80E2FF', edgecolors='#606060', marker='o', ax=axs['pitch'], hatch='///', label=away_team)
    scatter_goals = pitch.scatter(120-(goals2.x), 80-(goals2.y), s=(goals2.shot_statsbomb_xg * 900) + 100, c='white', edgecolors='black', marker='football', ax=axs['pitch'])
    title1 = axs['title'].text(0.5, 0.7, home_team+" vs "+away_team+"\n"+str(home_score) + " - " + str(away_score), color=pitch.line_color,
                           va='center', ha='center', fontproperties='Arial', fontsize=20)

    fig.legend()
    
    st.pyplot(fig)

