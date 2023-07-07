import streamlit as st
import pandas as pd
from statsbombpy import sb
import matplotlib.pyplot as plt
import numpy as np
from cssdetails import grow_element
import mplcursors

def render_radar_chart(match_choice, home_player_choice_id, home_player_choice, away_player_choice_id, away_player_choice):
    # Set the match ID and player IDs
    match_id = match_choice

    # Load the match data
    match_data = sb.events(match_id=match_id)

    # Filter events for Player 1
    player1_events = match_data[match_data['player_id'] == home_player_choice_id]

    # Filter events for Player 2
    player2_events = match_data[match_data['player_id'] == away_player_choice_id]

    # Calculate event frequencies for Player 1
    player1_event_counts = player1_events['type'].value_counts()

    # Calculate event frequencies for Player 2
    player2_event_counts = player2_events['type'].value_counts()

    # Combine the event frequencies into a DataFrame
    df = pd.DataFrame({'Player 1': player1_event_counts, 'Player 2': player2_event_counts}).fillna(0)

    # Get the event categories and their corresponding frequencies
    categories = df.index.tolist()
    values_player1 = df['Player 1'].values.tolist()
    values_player2 = df['Player 2'].values.tolist()

    # Number of categories
    num_categories = len(categories)

    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': 'polar'})

    # Set the angle and position of each category on the radar chart
    angles = np.linspace(0, 2 * np.pi, num_categories, endpoint=False).tolist()
    angles += angles[:1]

    # Plot the radar chart for Player 1
    ax.plot(angles, values_player1 + values_player1[:1], linewidth=1, linestyle='solid', label=home_player_choice)
    ax.fill(angles, values_player1 + values_player1[:1], alpha=0.25)

    # Plot the radar chart for Player 2
    ax.plot(angles, values_player2 + values_player2[:1], linewidth=1, linestyle='solid', label=away_player_choice)
    ax.fill(angles, values_player2 + values_player2[:1], alpha=0.25)

    # Set the angle ticks and labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # Set the radial axis label
    ax.set_yticklabels([])

    # Add a legend
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    mplcursors.cursor(hover=True).connect("add", lambda event: event.annotation.set_text(event.artist.get_label()))


    st.pyplot(fig)
    grow_element(st)
