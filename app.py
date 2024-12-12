from flask import Flask, render_template, jsonify
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguestandings
import pandas as pd
from math import floor
import os
import numpy as np

# Initialize Flask app
app = Flask(__name__)

PICKS_DATA = [
    {
        'Team': 'Boston Celtics',
        'O/U': 58.5,
        'MT Picks': 'U',
        'CH Picks': 'O',
        'RT Picks': 'O'
    },
    {
        'Team': 'New York Knicks ',
        'O/U': 53.5,
        'MT Picks': 'O',
        'CH Picks': 'O',
        'RT Picks': 'O'
    },
    {
        'Team': 'Philadelphia 76ers',
        'O/U': 50.5,
        'MT Picks': 'O',
        'CH Picks': 'U',
        'RT Picks': 'U'
    },
    {
        'Team': 'Brooklyn Nets',
        'O/U': 19.5,
        'MT Picks': 'U',
        'CH Picks': 'U',
        'RT Picks': 'U'
    },
    {
        'Team': 'Toronto Raptors',
        'O/U': 29.5,
        'MT Picks': 'U',
        'CH Picks': 'U',
        'RT Picks': 'U'
    },
    {
        'Team': 'Central ',
        'O/U': np.nan,
        'MT Picks': 'nan',
        'CH Picks': 'nan',
        'RT Picks': 'nan'
    },
    {
        'Team': 'Milwaukee Bucks',
        'O/U': 49.5,
        'MT Picks': 'U',
        'CH Picks': 'O',
        'RT Picks': 'U'
    },
    {
        'Team': 'Cleveland Cavaliers ',
        'O/U': 48.5,
        'MT Picks': 'O',
        'CH Picks': 'U',
        'RT Picks': 'O'
    },
    {
        'Team': 'Indiana Pacers',
        'O/U': 46.5,
        'MT Picks': 'O',
        'CH Picks': 'O',
        'RT Picks': 'O'
    },
    {
        'Team': 'Chiacgo Bulls',
        'O/U': 28.5,
        'MT Picks': 'U',
        'CH Picks': 'U',
        'RT Picks': 'U'
    },
    {
        'Team': 'Detroit Pistons',
        'O/U': 25.5,
        'MT Picks': 'U',
        'CH Picks': 'O',
        'RT Picks': 'O'
    },
    {
        'Team': 'Southeast',
        'O/U': np.nan,
        'MT Picks': 'nan',
        'CH Picks': 'nan',
        'RT Picks': 'nan'
    },
    {
        'Team': 'Orlando Magic',
        'O/U': 47.5,
        'MT Picks': 'O',
        'CH Picks': 'O',
        'RT Picks': 'U'
    },
    {
        'Team': 'Miami Heat',
        'O/U': 43.5,
        'MT Picks': 'U',
        'CH Picks': 'U',
        'RT Picks': 'O'
    },
    {
        'Team': 'Atlanta Hawks',
        'O/U': 36.5,
        'MT Picks': 'U',
        'CH Picks': 'O',
        'RT Picks': 'U'
    },
    {
        'Team': 'Charlotte Hornets',
        'O/U': 31.5,
        'MT Picks': 'O',
        'CH Picks': 'O',
        'RT Picks': 'U'
    },
    {
        'Team': 'Washington Wizards',
        'O/U': 19.5,
        'MT Picks': 'U',
        'CH Picks': 'U',
        'RT Picks': 'O'
    },
    {
        'Team': 'Western Conference',
        'O/U': np.nan,
        'MT Picks': 'nan',
        'CH Picks': 'nan',
        'RT Picks': 'nan'
    },
    {
        'Team': 'Northwest',
        'O/U': np.nan,
        'MT Picks': 'nan',
        'CH Picks': 'nan',
        'RT Picks': 'nan'
    },
    {
        'Team': 'Oklahoma City Thunder ',
        'O/U': 57.5,
        'MT Picks': 'O',
        'CH Picks': 'U',
        'RT Picks': 'U'
    },
    {
        'Team': 'Denver Nuggets',
        'O/U': 50.5,
        'MT Picks': 'U',
        'CH Picks': 'O',
        'RT Picks': 'O'
    },
    {
        'Team': 'Minnesota Timberwolves',
        'O/U': 51.5,
        'MT Picks': 'U',
        'CH Picks': 'O',
        'RT Picks': 'O'
    },
    {
        'Team': 'Utah Jazz',
        'O/U': 27.5,
        'MT Picks': 'U',
        'CH Picks': 'U',
        'RT Picks': 'U'
    },
    {
        'Team': 'Portland Trail Blazers',
        'O/U': 20.5,
        'MT Picks': 'U',
        'CH Picks': 'U',
        'RT Picks': 'U'
    },
    {
        'Team': 'Pacific ',
        'O/U': np.nan,
        'MT Picks': 'nan',
        'CH Picks': 'nan',
        'RT Picks': 'nan'
    },
    {
        'Team': 'Los Angeles Clippers',
        'O/U': 35.5,
        'MT Picks': 'O',
        'CH Picks': 'O',
        'RT Picks': 'U'
    },
    {
        'Team': 'Phoenix Suns',
        'O/U': 48.5,
        'MT Picks': 'O',
        'CH Picks': 'O',
        'RT Picks': 'O'
    },
    {
        'Team': 'Los Angeles Lakers',
        'O/U': 42.5,
        'MT Picks': 'O',
        'CH Picks': 'O',
        'RT Picks': 'O'
    },
    {
        'Team': 'Sacramento Kings ',
        'O/U': 46.5,
        'MT Picks': 'U',
        'CH Picks': 'U',
        'RT Picks': 'U'
    },
    {
        'Team': 'Golden State Warriors',
        'O/U': 43.5,
        'MT Picks': 'O',
        'CH Picks': 'U',
        'RT Picks': 'O'
    },
    {
        'Team': 'Southwest',
        'O/U': np.nan,
        'MT Picks': 'nan',
        'CH Picks': 'nan',
        'RT Picks': 'nan'
    },
    {
        'Team': 'Dallas Mavericks',
        'O/U': 48.5,
        'MT Picks': 'O',
        'CH Picks': 'O',
        'RT Picks': 'O'
    },
    {
        'Team': 'New Orleans Pelicans',
        'O/U': 45.5,
        'MT Picks': 'U',
        'CH Picks': 'U',
        'RT Picks': 'U'
    },
    {
        'Team': 'Houston Rockets',
        'O/U': 42.5,
        'MT Picks': 'O',
        'CH Picks': 'O',
        'RT Picks': 'U'
    },
    {
        'Team': 'Memphis Grizzlies',
        'O/U': 46.5,
        'MT Picks': 'O',
        'CH Picks': 'U',
        'RT Picks': 'U'
    },
    {
        'Team': 'San Antonio Spurs',
        'O/U': 35.5,
        'MT Picks': 'U',
        'CH Picks': 'O',
        'RT Picks': 'U'
    },
    {
        'Team': 'Tiebreaker',
        'O/U': np.nan,
        'MT Picks': 'nan',
        'CH Picks': 'nan',
        'RT Picks': 'nan'
    },
    {
        'Team': 'ECF Winner',
        'O/U': np.nan,
        'MT Picks': 'New York Knicks',
        'CH Picks': 'Boston Celtics',
        'RT Picks': 'New York Knicks'
    },
    {
        'Team': 'WCF Winner',
        'O/U': np.nan,
        'MT Picks': 'OKC Thunder',
        'CH Picks': 'OKC Thunder',
        'RT Picks': 'Dallas Mavericks'
    },
    {
        'Team': 'Finals Winner',
        'O/U': np.nan,
        'MT Picks': 'New York Knicks',
        'CH Picks': 'Boston Celtics',
        'RT Picks': 'New York Knicks'
    },
]

# Convert hardcoded data to DataFrame
over_under_data = pd.DataFrame(PICKS_DATA)
# Filter out rows with nan values and conference/division headers
over_under_data = over_under_data[
    over_under_data['O/U'].notna() & 
    ~over_under_data['Team'].str.contains('Conference|Division|Tiebreaker|Winner|Southeast|Pacific|Southwest|Northwest|Central', na=False)
].reset_index(drop=True)

# Define minimal team name mapping for the exceptions
TEAM_NAME_MAP = {
    'Blazers': 'Trail Blazers'  # This is the only difference that needs mapping
}

# Extract only team names (strip city names)
def extract_team_name(full_name):
    return full_name.split()[-1] if ' ' in full_name else full_name

over_under_data['Team'] = over_under_data['Team'].apply(
    lambda x: TEAM_NAME_MAP.get(extract_team_name(x), extract_team_name(x))
)

# Helper function to fetch win percentages
def fetch_win_percentages():
    standings = leaguestandings.LeagueStandings().get_data_frames()[0]
    # Print the team names from the API for debugging
    print("API Team Names:", standings['TeamName'].tolist())
    standings = standings[['TeamName', 'WinPCT']]
    standings['WinPCT'] = standings['WinPCT'].astype(float)
    return standings

# Calculate projections and grades
def calculate_projections():
    standings = fetch_win_percentages()
    merged_data = over_under_data.merge(standings, left_on='Team', right_on='TeamName', how='left')
    
    merged_data['Projected Wins'] = merged_data['WinPCT'].apply(lambda x: floor(x * 82))
    merged_data['Grade'] = merged_data.apply(
        lambda row: 'On Track' if row['Projected Wins'] >= row['O/U'] else 'Off Track', 
        axis=1
    )
    return merged_data[['Team', 'O/U', 'WinPCT', 'Projected Wins', 'Grade']]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/projections')
def projections():
    data = calculate_projections()
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/all_data')
def all_data():
    over_under_data.dropna(inplace=True)

    # Get projections data
    projections_data = calculate_projections()
    
    # Merge with original over_under_data
    complete_data = over_under_data.merge(
        projections_data[['Team', 'WinPCT', 'Projected Wins', 'Grade']], 
        on='Team', 
        how='left'
    )
    print(complete_data)
    return jsonify(complete_data.to_dict(orient='records'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)