import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patches
from bs4 import BeautifulSoup
import requests
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize
from make_dfs import dataframes
from card_parts import percentile_graph, header, statstable, release_point, pitching_points, arrival_points

bowler_statistics_df, bowler_statistics_percentile, stat_names, release_point_df, ball_pitching_df, arrival_point_df = dataframes(2025)
current_stats_df = pd.read_csv('data/CountyChamp25CricinfoUpdated.csv')

@st.cache_data
def bowler_card(bowler_name, current_stats_df):
    
    bowler_stats = bowler_statistics_df[bowler_statistics_df['Bowler'] == bowler_name]
    bowler_stats_list_unrounded = bowler_stats.iloc[0].tolist()[3:]
    bowler_stats_list = [round(x,2) for x in bowler_stats_list_unrounded]
    bowler_percentiles = bowler_statistics_percentile[bowler_statistics_percentile['Bowler'] == bowler_name]
    bowler_percentiles['Middle Percentage'] = 1 - bowler_percentiles['Middle Percentage']
    bowler_percentiles_list = bowler_percentiles.iloc[0].tolist()[3:]

    bowler_percentiles_list_percentages = [round(100*x, 0) for x in bowler_percentiles_list]
    colours = [plt.cm.Blues(x) for x in bowler_percentiles_list]

    fig, ax = plt.subplots(figsize = (11.69,16.54))
    fig.clf()
    fig.set_facecolor("#05092C")
    gs = GridSpec(10, 4, figure=fig)
    ax_header = fig.add_subplot(gs[0:1, 0:4])
    header(bowler_name, current_stats_df, ax_header)

    ax_table = fig.add_subplot(gs[1:2, :])
    statstable(bowler_name, current_stats_df, ax_table)
    ax_percentile = fig.add_subplot(gs[2:6, :])
    percentile_graph(stat_names, bowler_percentiles_list_percentages, colours, bowler_stats_list, ax_percentile)

    ax_release = fig.add_subplot(gs[6:10, 0:1])
    release_point(bowler_name, release_point_df, ax_release)

    ax_pitch = fig.add_subplot(gs[6:10, 1:2])
    pitching_points(bowler_name, ball_pitching_df, ax_pitch)

    ax_arrival = fig.add_subplot(gs[6:10, 2:4])
    arrival_points(bowler_name, arrival_point_df, ax_arrival)
    
    # plt.savefig('trial.png', dpi=300, bbox_inches='tight')
    # plt.show()
    return fig



st.title("Bowler Cards Web App")
bowler_name = st.selectbox("Select a Bowler", current_stats_df['Name'].unique())

if st.button("Generate Bowler Card"):
    fig = bowler_card(bowler_name, current_stats_df)
    st.pyplot(fig)