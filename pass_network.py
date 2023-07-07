import streamlit as st
import pandas as pd
import numpy as np
from mplsoccer import Pitch
from statsbombpy import sb
import mpld3

def display_pass_network(match_id, team_name):
    # Retrieving the event data
    df = sb.events(match_id)
    
    # Preparing the data
    sub = df.loc[(df["type"] == "Substitution") & (df["team"] == team_name)].index[0]
    df_pass = df.loc[(df["type"] == "Pass") & (df["team"] == team_name) & (df.index < sub),
                     ['location', 'pass_outcome', 'player', 'pass_end_location', 'pass_recipient']]

    # Extracting the necessary columns
    df_pass["player_name"] = df_pass["player"].apply(lambda x: x.split()[-1])
    df_pass["pass_recipient_name"] = df_pass["pass_recipient"].apply(lambda x: str(x).split()[-1] if isinstance(x, str) else "")

    # Calculating vertices size and location
    scatter_df = pd.DataFrame()
    for i, name in enumerate(df_pass["player_name"].unique()):
        passx = df_pass.loc[df_pass["player_name"] == name, "location"].apply(lambda x: x[0]).to_numpy()
        recx = df_pass.loc[df_pass["pass_recipient_name"] == name, "pass_end_location"].apply(lambda x: x[0]).to_numpy()
        passy = df_pass.loc[df_pass["player_name"] == name, "location"].apply(lambda x: x[1]).to_numpy()
        recy = df_pass.loc[df_pass["pass_recipient_name"] == name, "pass_end_location"].apply(lambda x: x[1]).to_numpy()
        scatter_df.at[i, "player_name"] = name
        scatter_df.at[i, "x"] = np.mean(np.concatenate([passx, recx]))
        scatter_df.at[i, "y"] = np.mean(np.concatenate([passy, recy]))
        scatter_df.at[i, "no"] = df_pass.loc[df_pass["player_name"] == name].shape[0]

    # Adjusting the size of circles
    scatter_df['marker_size'] = (scatter_df['no'] / scatter_df['no'].max() * 1500)

    # Calculating edges width
    df_pass["pair_key"] = df_pass.apply(lambda x: "_".join(sorted([x["player_name"], x["pass_recipient_name"]])), axis=1)
    lines_df = df_pass.groupby(["pair_key"]).size().reset_index(name='pass_count')
    lines_df = lines_df[lines_df['pass_count'] > 2]

    # Plotting vertices
    pitch = Pitch(pitch_color='grass', line_color='white')
    fig, ax = pitch.draw(figsize=(10, 6.5))
    
    pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='black', edgecolors='grey', linewidth=1, alpha=1, ax=ax)
    for i, row in scatter_df.iterrows():
        pitch.annotate(row.player_name, xy=(row.x, row.y), c='white', va='center', ha='center', weight="bold", size=5, ax=ax)

    # Adding pass count and line width information
    for i, row in lines_df.iterrows():
        player1 = row["pair_key"].split("_")[0]
        player2 = row['pair_key'].split("_")[1]
        
        # Check if player1 exists in scatter_df
        if player1 in scatter_df["player_name"].values:
            player1_x = scatter_df.loc[scatter_df["player_name"] == player1]['x'].iloc[0]
            player1_y = scatter_df.loc[scatter_df["player_name"] == player1]['y'].iloc[0]
        else:
            continue  # Skip to the next iteration if player1 doesn't exist

        # Check if player2 exists in scatter_df
        if player2 in scatter_df["player_name"].values:
            player2_x = scatter_df.loc[scatter_df["player_name"] == player2]['x'].iloc[0]
            player2_y = scatter_df.loc[scatter_df["player_name"] == player2]['y'].iloc[0]
        else:
            continue  # Skip to the next iteration if player2 doesn't exist

        num_passes = row["pass_count"]
        line_width = (num_passes / lines_df['pass_count'].max() * 10)
        
        pitch.lines(player1_x, player1_y, player2_x, player2_y, alpha=1, lw=line_width, zorder=2, color="black", ax=ax)
        
        # Annotate the lines with pass count
        x_mid = (player1_x + player2_x) / 2
        y_mid = (player1_y + player2_y) / 2
        ax.annotate(f"{num_passes}", xy=(x_mid, y_mid), c='black', va='center', ha='center', weight="bold", size=8)

    # Adjust figure size and margins
    fig.set_figwidth(8)
    fig.set_figheight(5)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    # Display the Pass Network plot
    st.pyplot(fig)