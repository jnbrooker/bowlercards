import pandas as pd
from datetime import datetime
from scipy.stats import rankdata
import matplotlib.pyplot as plt

def bowler_data(bowler_name, filtered_df, average_release_x):
    bowler_df = filtered_df[filtered_df['Bowler'] == bowler_name]

    bowler_type = bowler_df['Bowler Type'].iloc[0]

    # Average Adjusted Velocity

    aav_df = bowler_df[(bowler_df['ReleaseX External'].notna()) & (bowler_df['Speed External'].notna())]
    aav_df['Adjusted Velocity'] = aav_df['Speed External'] * average_release_x/aav_df['ReleaseX External']

    mean = aav_df['Adjusted Velocity'].mean()
    mean_90th = aav_df[aav_df['Adjusted Velocity'] >= aav_df['Adjusted Velocity'].quantile(0.9)]['Adjusted Velocity'].mean()
    mean_10th = aav_df[aav_df['Adjusted Velocity'] <= aav_df['Adjusted Velocity'].quantile(0.1)]['Adjusted Velocity'].mean()
    mean_diff = mean_90th - mean_10th

    # Average Release Height

    rh_mean = bowler_df[bowler_df['ReleaseZ External'].notna()]['ReleaseZ External'].mean()

    # Middle, Whiff and Edge Percentage

    shots_df = bowler_df[~bowler_df['Shot'].isin(['Padded Away', 'No Shot'])]
    shots_df = shots_df[shots_df['Shot'].notna()]
    edges_df = shots_df[shots_df['Connection'].isin(['Thick Edge', 'Inside Edge', 'Outside Edge','Leading Edge', 'Top Edge', 'Bottom Edge'])]
    swings = len(shots_df)
    middle_percentage = len(shots_df[shots_df['Connection'] == 'Middled'])/swings
    edge_percentage = len(edges_df)/swings
    whiff_percentage = len(shots_df[shots_df['Connection'] == 'Missed'])/swings

    runs_per_edge = edges_df['Runs'].mean()

    return bowler_type, mean, mean_90th, mean_diff, rh_mean, middle_percentage, edge_percentage, whiff_percentage, runs_per_edge



def dataframes(year):
    full_df = pd.read_csv('data/Champo2325.csv')
    full_df['Date'] = pd.to_datetime(full_df['Date'], format='%d/%m/%Y')
    filtered_df = full_df[(full_df['Date'] > datetime.strptime(f'01/01/{year}', '%d/%m/%Y')) & 
                          (full_df['Date'] < datetime.strptime(f'31/12/{year}', '%d/%m/%Y'))]
    

    print(filtered_df['Bowler Type'].unique().tolist())

    spinner_types = ['ROB', 'LOB', 'LLB', 'RLB']
    fast_bowler_types = ['RFM', 'RF', 'RM', 'LM', 'LFM', 'WK']

    # shots = filtered_df['Shot'].unique().tolist()
    # print(shots)

    # Average Adjusted Velocity & 90th Percentile Adjusted Velocity & Variation between the 90th & 10th Percentile
    # Bowling speed adjusted for the distance they were bowling from by release point in front of crease

    # Average Release Height

    # Middle Percentage, Whiff Percentage and Edge Percentage
    # Runs per edge

    # Percentiles for all as well

    bowlers = filtered_df['Bowler'].unique().tolist()
    average_release_x = filtered_df['ReleaseX External'].mean()
    bowler_statistics_df = pd.DataFrame()

    for index, bowler_name in enumerate(bowlers):
        bowler_type, average_adjusted_velocity, adjusted_velocity_90, adjusted_velocity_variation, average_release_height, middle_percentage, edge_percentage, whiff_percentage, runs_per_edge= bowler_data(bowler_name, filtered_df, average_release_x)

        bowler_statistics_df.loc[index, 'Bowler'] = bowler_name
        bowler_statistics_df.loc[index, 'Bowler Type'] = bowler_type
        bowler_statistics_df['Short Type'] = bowler_statistics_df['Bowler Type'].apply(lambda x: 'Seam' if x in fast_bowler_types else 'Spin')
        bowler_statistics_df.loc[index, 'Average Adjusted Velocity'] = average_adjusted_velocity
        bowler_statistics_df.loc[index, '90th Percentile Adjusted Velocity'] = adjusted_velocity_90
        bowler_statistics_df.loc[index, 'Adjusted Velocity Variation'] = adjusted_velocity_variation
        bowler_statistics_df.loc[index, 'Average Release Height'] = average_release_height
        bowler_statistics_df.loc[index, 'Middle Percentage'] = middle_percentage
        bowler_statistics_df.loc[index, 'Edge Percentage'] = edge_percentage
        bowler_statistics_df.loc[index, 'Whiff Percentage'] = whiff_percentage
        bowler_statistics_df.loc[index, 'Runs per Edge'] = runs_per_edge

    # Making Percentile dataframe

    bowler_statistics_percentile = bowler_statistics_df.copy()
    stat_names = ['Average Adjusted Velocity', '90th Percentile Adjusted Velocity', 'Adjusted Velocity Variation', 'Average Release Height',
                  'Middle Percentage', 'Edge Percentage', 'Whiff Percentage', 'Runs per Edge']
    bowler_statistics_percentile[stat_names] = bowler_statistics_df.groupby('Short Type')[stat_names].rank(pct=True)

    # print(bowler_statistics_df.head())
    # print(bowler_statistics_percentile.head())

    release_point_df = filtered_df[['Bowler', 'ReleaseY External', 'ReleaseZ External']]
    release_point_df = release_point_df.dropna()

    ball_pitching_df = filtered_df[['Bowler', 'External PitchX', 'External PitchY']]
    ball_pitching_df = ball_pitching_df.dropna()

    arrival_point_df = filtered_df[['Bowler', 'Analyst Arrival Line', 'Analyst Arrival Height']]
    arrival_point_df = arrival_point_df.dropna()

    return bowler_statistics_df, bowler_statistics_percentile, stat_names, release_point_df, ball_pitching_df, arrival_point_df


dataframes(2025)

