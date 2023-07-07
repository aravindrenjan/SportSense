import pandas as pd
from mplsoccer import Pitch
from statsbombpy import sb
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import streamlit as st

def display_kmeans(competition_id, season_id, match_id, home_player, away_player):
    temp = competition_id
    t2 = sb.matches(competition_id, season_id)
    t3 = sb.events(match_id)

    p1 = home_player
    p2 = away_player

    competitions = sb.competitions()
    uniq_pairs = list(competitions[['competition_id', 'season_id']].itertuples(index=False, name=None))

    pass_cols = ['duration', 'pass_angle', 'pass_body_part', 'pass_cross', 'pass_cut_back',
                 'pass_deflected', 'pass_height', 'pass_inswinging', 'pass_length',
                 'pass_shot_assist', 'pass_straight', 'pass_switch', 'pass_through_ball', 'pass_type',
                 'play_pattern', 'under_pressure','pass_end_location', 'pass_outcome', 'player']

    pass_data_p1 = pd.DataFrame(columns=pass_cols)
    pass_data_p2 = pd.DataFrame(columns=pass_cols)

    for i in uniq_pairs:
        try:
            mid, away_team = sb.matches(i[0], i[1])[['match_id', 'away_team']].iloc[0]
            events = sb.events(mid)
            pass_data = events[[i for i in pass_cols if i in events.columns]]
            pass_data = pass_data[pass_data['pass_angle'].notna()]
            pass_data.fillna(value=False, inplace=True)
            for col in pass_cols:
                if col not in pass_data.columns:
                    pass_data[col] = False
            pass_data['pass_outcome'] = pass_data['pass_outcome'].apply(lambda x: 'Complete' if x is False else 'Incomplete')

            pass_data_p1 = pd.concat([pass_data_p1, pass_data[pass_data['player'] == p1]], ignore_index=True)\
                .reset_index(drop=True)
            pass_data_p2 = pd.concat([pass_data_p2, pass_data[pass_data['player'] == p2]], ignore_index=True)\
                .reset_index(drop=True)
        except Exception as ex:
            pass

    # Concatenate pass data for both players
    pass_data = pd.concat([pass_data_p1, pass_data_p2], ignore_index=True)

    # Select features for clustering
    selected_features = ['duration', 'pass_angle', 'pass_length']

    # Preprocess the data
    pass_data_selected = pass_data[selected_features]
    scaler = StandardScaler()
    pass_data_scaled = scaler.fit_transform(pass_data_selected)

    # Perform k-means clustering
    kmeans = KMeans(n_clusters=2, random_state=0)
    kmeans.fit(pass_data_scaled)
    cluster_labels = kmeans.labels_

    # Add cluster labels to the pass data
    pass_data['cluster'] = cluster_labels

    # Analyze the results
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)

    # Print the cluster centers
    # for cluster_idx, center in enumerate(cluster_centers):
    #     print(f"Cluster {cluster_idx + 1} Center:")
    #     for feature_idx, feature_name in enumerate(selected_features):
    #         print(f"{feature_name}: {center[feature_idx]}")

    # for cluster_idx, center in enumerate(cluster_centers):
    #     st.markdown(f"<h3>Cluster {cluster_idx + 1} Center:</h3>", unsafe_allow_html=True)
    #     for feature_idx, feature_name in enumerate(selected_features):
    #         st.markdown(f"<p>{feature_name}: {center[feature_idx]}</p>", unsafe_allow_html=True)

    # Visualize the clusters on a pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='#c7d5cc')
    fig, ax = pitch.draw()

    # Plot passes for each player with different colors based on the cluster
    legend_handles = []
    for player, color in zip([p1, p2], ['red', 'blue']):
        player_data = pass_data[pass_data['player'] == player]
        scatter = ax.scatter(player_data['pass_end_location'].apply(lambda x: x[0]), 
                             player_data['pass_end_location'].apply(lambda x: x[1]),
                             marker='o', color=color, edgecolors='black', linewidths=1, alpha=0.7)
        legend_handles.append(scatter)

    # Add legends
    legend_labels = [f'{p1}', f'{p2}']
    ax.legend(legend_handles, legend_labels, loc='upper right')

    # Add titles and axis labels
    ax.set_title('Passes Visualization')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')

    # Add gridlines
    ax.grid(True, linestyle='--', alpha=0.5)

    # Show the plot
    # st.pyplot(fig)
    return cluster_centers,selected_features,fig
