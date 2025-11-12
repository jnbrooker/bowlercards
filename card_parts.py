import pandas as pd
from datetime import datetime
from scipy.stats import rankdata
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox




def percentile_graph(stat_names, bowler_percentiles_list_percentages, colours, bowler_stats_list, ax):
    plt.sca(ax)
    ax.set_facecolor("#05092C")
    bars = ax.barh(stat_names[::-1], bowler_percentiles_list_percentages[::-1], color=colours[::-1])
    for bar, value, colour, true_value in zip(bars, bowler_percentiles_list_percentages[::-1], colours[::-1], bowler_stats_list[::-1]):
        x = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2

        ax.scatter(x + 0.5, y, s=1000, color=colour, edgecolors='black', zorder=5)
        ax.text(x + 0.55, y-0.01, str(value), ha='center', va='center', color='black', zorder=6, fontdict={''
        'family':'Courier', 'size':12})
        ax.text(112, y, str(true_value), ha='center', va='center', color='white', zorder=6, fontdict={''
        'family':'Courier', 'size':12})
        if bar != bars[0]:
           ax.hlines(y-0.5, xmin=-5, xmax=120, colors='white', linestyles='--')


    xmin, xmax = ax.get_xlim()
    ax.set_xlim(xmin-5, xmax-10)

    ymin, ymax = ax.get_ylim()
    ax.set_ylim(ymin, ymax)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(left=False, bottom=False)
    ax.set_xticklabels([])
    ax.grid(False)

    ticks = ['Adjusted Velo', '90 Pct AV', 'AV Variation',
                        'Release Height', 'Middle %', 'Edge %', 'Whiff %', 'Runs per Edge']

    ax.set_yticklabels(ticks[::-1])
    for tick in ax.get_yticklabels():
        tick.set_fontfamily('Courier')
        tick.set_fontsize(10)
        tick.set_color('white')
    ax.tick_params(axis='y', pad=-70)
    return ax

def header(bowler_name, current_stats_df, ax):
    current_player_stats = current_stats_df[current_stats_df['Name'] == bowler_name]
    team = current_player_stats['Team'].iloc[0]
    player_url = current_player_stats['Link'].iloc[0]
    player_picture_route = f"Bowling Cards/{player_url.split('/')[-1]}.jpg"

    try:
        img = mpimg.imread(player_picture_route)
        
        imagebox = OffsetImage(img, zoom=0.2)
        ab = AnnotationBbox(imagebox, (0.1, 0.9), frameon=False, xycoords='axes fraction')
        ax.add_artist(ab)
    except Exception as e:
        print(f"Could not load image: {e}")

    ax.text(0.5, 0.9, bowler_name, fontsize=24, color='white', fontweight='bold', va='center', ha='center', fontfamily='Courier', transform=ax.transAxes)
    ax.text(0.5, 0.5, team, fontsize=20, color='white', fontweight='bold', va='center', ha='center', fontfamily='Courier', transform=ax.transAxes)
    ax.axis("off")
    return ax

current_stats_df = pd.read_csv('data/CountyChamp25CricinfoUpdated.csv')
print(current_stats_df.columns)
# header('JA Porter', current_stats_df)

def statstable(bowler_name, current_stats_df, ax):
    current_player_stats = current_stats_df[current_stats_df['Name'] == bowler_name]
    table_contents = current_player_stats[['Mat', 'Inns', 'Balls', 'Overs', 'Mdns', 'Runs',
       'Wkts', 'Ave', 'Econ', 'SR', '4', '5']]
    ax.axis('off')
    rows, cols = table_contents.shape
    cell_colours = [["#9ac8e0"] * cols for _ in range(rows)]
    table = plt.table(cellText=table_contents.values,
                      colLabels=table_contents.columns,
                      cellLoc='center', 
                      loc='center',
                      colColours=["#084a91"] * len(table_contents.columns),
                      cellColours=cell_colours)
    
    table.scale(1, 4)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    for (row, col), cell in table.get_celld().items():
        cell.get_text().set_fontfamily('Courier')
        cell.get_text().set_fontsize(12)
        cell.get_text().set_color('black')
    
    return table

def release_point(bowler_name, df, ax):
    league_average_release = df['ReleaseZ External'].mean()
    player_df = df[df['Bowler'] == bowler_name]
    ax.set_facecolor('#05092C')
    ax.scatter(player_df['ReleaseY External'], player_df['ReleaseZ External'], 
               color="#9ac8e0", alpha=0.7, s=10)
    ax.axhline(y=league_average_release, color='white', linestyle='--', linewidth=1.5, label='League Avg')
    ax.set_xlim(-1.83, 1.83)
    ax.set_ylim(0, 2.5)
    ax.set_title('Release Points', color='white', fontname='Courier')
    for spine in ax.spines.values():
        spine.set_color('white')
    
    ax.tick_params(axis='both', which='both', length=0, labelcolor='white')
    ax.set_xticks([])
    ax.set_yticks([])
    return ax

def pitching_points(bowler_name, df, ax):
    player_df = df[df['Bowler'] == bowler_name]
    ax.set_facecolor('#05092C')
    ax.scatter(player_df['External PitchY'], player_df['External PitchX'], 
               color="#9ac8e0", alpha=0.7, s=10)
    ax.set_xlim(-1.83, 1.83)
    ax.set_ylim(0, 20.12)
    ax.invert_yaxis()
    ax.set_title('Pitching Points', color='white', fontname='Courier')
    for spine in ax.spines.values():
        spine.set_color('white')
    
    ax.tick_params(axis='both', which='both', length=0, labelcolor='white')
    ax.axhline(y=2, color='white', linestyle='--', linewidth=1.5, label='Yorker')
    ax.axhline(y=4, color='white', linestyle='--', linewidth=1.5, label='Full')
    ax.axhline(y=8, color='white', linestyle='--', linewidth=1.5, label='Good')
    ax.set_xticks([])
    ax.set_yticks([])
    return ax

def arrival_points(bowler_name, df, ax):
    player_df = df[df['Bowler'] == bowler_name]
    ax.set_facecolor('#05092C')
    ax.scatter(player_df['Analyst Arrival Line'], player_df['Analyst Arrival Height'], 
               color="#9ac8e0", alpha=0.7, s=10)
    ax.set_xlim(-1.83, 1.83)
    ax.set_ylim(0, 2.5)
    ax.set_title('Arrival Points', color='white', fontname='Courier')
    for spine in ax.spines.values():
        spine.set_color('white')
    
    ax.tick_params(axis='both', which='both', length=0, labelcolor='white')
    ax.axhline(y=0.712, color='white', linestyle='--', linewidth=1.5, label='Stumps')
    ax.axvline(x=-0.114, color='white', linestyle='--', linewidth=1.5, label='Stumps')
    ax.axvline(x=0.114, color='white', linestyle='--', linewidth=1.5, label='Stumps')
    ax.set_xticks([])
    ax.set_yticks([])
    return ax