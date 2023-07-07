import streamlit as st
import pandas as pd
import plotly.express as px
from statsbombpy import sb
from mplsoccer import Pitch
from scipy.ndimage import gaussian_filter
import cmasher as cmr

def prepare_pressure_data(pressure,team_name):
    pressure = pressure[['team', 'player', 'location']]
    pressure = pressure[pressure.team == team_name]
    pressure['x'] = pressure.location.apply(lambda x: x[0])
    pressure['y'] = pressure.location.apply(lambda x: x[1])
    pressure = pressure.drop('location', axis=1)
    return pressure


def render_pressure_heatmap(pressure):
    pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='#efefef')
    # fig, axs = pitch.grid(figheight=4, title_height=0.08, endnote_space=0, axis=False, title_space=0, grid_height=0.82, endnote_height=0.05)
    fig, axs = pitch.grid(
        figheight=7,
        title_height=0.08,
        endnote_space=0,
        axis=False,
        title_space=0,
        grid_height=0.82,
        endnote_height=0.05,
    )
    fig.set_facecolor('white')
    bin_statistic = pitch.bin_statistic(pressure.x, pressure.y, statistic='count', bins=(25, 25))
    bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)
    pcm = pitch.heatmap(bin_statistic, ax=axs['pitch'], cmap=cmr.lavender, edgecolors='#22312b')

    cbar = fig.colorbar(pcm, ax=axs['pitch'], shrink=0.6)
    cbar.outline.set_edgecolor('#efefef')
    # Adjust figure size and margins
    fig.set_figwidth(40)
    fig.set_figheight(30)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=0.2)

    st.pyplot(fig)
