import streamlit as st
import pandas as pd
from statsbombpy import sb
from kmeans import display_kmeans
# class imports

from radar_chart import render_radar_chart
from shots_chart import prepare_shots_data, render_shots_chart
from heatmap import prepare_pressure_data, render_pressure_heatmap
from pass_network import display_pass_network
from player_pass_net import display_player_pass_network
from cssdetails import set_font_css, set_padding_css, grow_element, title_alignment, page_details

# Adjust the margin of the Streamlit web page
st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="SportSense Football Dashboard", page_icon=":soccer:")
# set_padding_css(st)

def main():
    # Page title
    with st.container():
        page_details(st)
        title_alignment(st)
        competitions_data = sb.competitions()

        # Create a dictionary to store competition-season-match data
        comp_dict = {}
        comp_name_dict = {}

        # Iterate over competition IDs
        for competition_id, competition_name in zip(competitions_data['competition_id'], competitions_data['competition_name']):
            season_ids = list(competitions_data.loc[competitions_data['competition_id'] == competition_id, 'season_id'])
            comp_dict[competition_id] = {season_id: {} for season_id in season_ids}
            comp_name_dict[competition_id] = competition_name

        # Iterate over competitions and seasons to retrieve match data

        for competition_id in comp_dict:
            for season_id in comp_dict[competition_id]:
                try:
                    matches = sb.matches(competition_id=competition_id, season_id=season_id)
                    match_ids = matches['match_id'].tolist()
                    comp_dict[competition_id][season_id] = match_ids
                except:
                    pass
    
    with st.container():
        col1, col2, col3 = st.columns((1,1,1))
    
        with col1:
            set_font_css(st,24)
            # Competition selection
            selected_competition = st.selectbox(
                    "Select Competition",
                    list(comp_name_dict.values()),
                    format_func=lambda x: x,
                    key="competition_select"
                )
            selected_competition_id = list(comp_name_dict.keys())[list(comp_name_dict.values()).index(selected_competition)]
        with col2:
            set_font_css(st,18)
            with st.container():
            # Apply custom CSS styling
            # Season selection
                selected_season_id = st.selectbox("Select Season", list(comp_dict[selected_competition_id].keys()))

        with col3:
            set_font_css(st,18)
            with st.container():
            # Retrieve matches data
                match_id_name = {}
                matches_data = sb.matches(competition_id=selected_competition_id, season_id=selected_season_id)
                matches = matches_data['match_id'].tolist()

                for row_id, match_row in matches_data.iterrows():
                    match_id = match_row['match_id']
                    home_team = match_row['home_team']
                    away_team = match_row['away_team']
                    match_name = f"{home_team} vs {away_team}"
                    match_id_name[match_id] = match_name

            # Match selection
                selected_match_id = st.selectbox("Select Match", list(match_id_name.keys()), format_func=lambda x: match_id_name[x], index=0)
                selected_match = match_id_name[selected_match_id]

                # Retrieve team names for the selected match
                match_data = sb.matches(competition_id=selected_competition_id, season_id=selected_season_id)

                selected_match_data = matches_data[matches_data['match_id'] == selected_match_id]
                if len(selected_match_data) > 0:
                    home_team = match_data.loc[match_data['match_id'] == selected_match_id, 'home_team'].values[0]
                    away_team = match_data.loc[match_data['match_id'] == selected_match_id, 'away_team'].values[0]
                    home_score = match_data.loc[match_data['match_id'] == selected_match_id, 'home_score'].values[0]
                    away_score = match_data.loc[match_data['match_id'] == selected_match_id, 'away_score'].values[0]

    my_expander = st.expander("Click to View the Shots Chart! :soccer:", expanded=False)
    with my_expander:
        shots = sb.events(match_id=selected_match_id)
        shots = shots[shots['type'] == 'Shot']
        render_shots_chart(shots, home_team, away_team, home_score, away_score)

    with st.container():
        set_font_css(st,18)
        team_choice = st.selectbox("Select Team", [home_team, away_team])
        set_padding_css(st)

        col1, col2 = st.columns(2)
        with col1:
            my_expander = st.expander("Click to View "+team_choice+"'s the Pass Network! :runner:", expanded=False)
            with my_expander:
                st.subheader("Pass Network")
                display_pass_network(selected_match_id, team_choice)
                
        with col2:
            my_expander = st.expander("Click to View "+team_choice+"'s Defensive Pressure! :runner:", expanded=False)
            with my_expander:
                st.subheader("Pressure Heatmap")
                # Retrieve pressure data
                pressure_data = sb.events(match_id=selected_match_id)
                pressure_data = pressure_data[pressure_data['type'] == 'Pressure']
                pressure_data = pressure_data[pressure_data.team == team_choice]
                pressure_data = prepare_pressure_data(pressure_data, team_choice)
                render_pressure_heatmap(pressure_data)

    with st.container():
        col1, col2 = st.columns(2)            
        with col1:
                set_font_css(st,18)
                # Lineup selection
                lineups = sb.lineups(selected_match_id)
                home_players = lineups[home_team]['player_name']
                # Additional lines for player selection dropdown menus
                home_player_choice = st.selectbox("Select Home Team Player", home_players)

        with col2:
                set_font_css(st,18)
                # Lineup selection
                lineups = sb.lineups(selected_match_id)
                away_players = lineups[away_team]['player_name']
                # Additional lines for player selection dropdown menus
                away_player_choice = st.selectbox("Select Away Team Player", away_players)
        
                home_player_choice_id = 0
                away_player_choice_id = 0
                for team_name, lineup in lineups.items():
                    if team_name == home_team:
                        home_player_choice_id = int(lineup[lineup['player_name'] == home_player_choice]['player_id'].values[0])
                    elif team_name == away_team:
                        away_player_choice_id = int(lineup[lineup['player_name'] == away_player_choice]['player_id'].values[0])
    with st.container():
        col1, col2, col3 = st.columns(3)          
        with col2:
            my_expander = st.expander("Let's Compare these Players!", expanded=False)
            with my_expander:
                # Render the radar chart for player comparison
                st.subheader("Player Comparison")
                grow_element(st)
                render_radar_chart(selected_match_id, home_player_choice_id, home_player_choice, away_player_choice_id, away_player_choice)
                
        with col1:
            my_expander = st.expander("Here is the "+ home_player_choice+"'s Pass Network!", expanded=False)
            with my_expander:
                st.subheader("Player Pass Network - " + home_player_choice)
                display_player_pass_network(selected_match_id, home_player_choice)

        with col3:
            my_expander = st.expander("Here is the "+ away_player_choice+"'s Pass Network!", expanded=False)
            with my_expander:
                st.subheader("Player Pass Network - " + away_player_choice)
                display_player_pass_network(selected_match_id, away_player_choice)
    
    cluster_centers, selected_features, figkmeans = display_kmeans(selected_competition_id, selected_season_id, selected_match_id, home_player_choice, away_player_choice)
    
    with st.container():
        st.markdown(
    """
    <h4 style="text-align: center;">Player Pass Clusters (using K-Means)</h4>
    """,
    unsafe_allow_html=True
)

        col1, col2 = st.columns(2)          
        with col1:        
            cluster_idx = 0
            center = cluster_centers[cluster_idx]
            st.markdown(f"<h5 style='display: flex; text-align: center; align-items: center; justify-content: center;'>{home_player_choice}'s Cluster</h5>", unsafe_allow_html=True)
            for feature_idx, feature_name in enumerate(selected_features):
                rounded_value = round(center[feature_idx], 2)
                st.markdown(f"<p style='display: flex; text-align: center; align-items: center; justify-content: center;'>{feature_name}: {rounded_value}</p>", unsafe_allow_html=True)
        with col2:
            cluster_idx = 1
            center = cluster_centers[cluster_idx]
            st.markdown(f"<h5 style='display: flex; text-align: center; align-items: center; justify-content: center;'>{away_player_choice}'s Cluster</h5>", unsafe_allow_html=True)
            for feature_idx, feature_name in enumerate(selected_features):
                rounded_value = round(center[feature_idx], 2)
                st.markdown(f"<p style='display: flex; text-align: center; align-items: center; justify-content: center;'>{feature_name}: {rounded_value}</p>", unsafe_allow_html=True)

    my_expander = st.expander("Players Pass K-Means Clustering", expanded=False)
    with my_expander:
        st.pyplot(figkmeans)

if __name__ == "__main__":
    main()
