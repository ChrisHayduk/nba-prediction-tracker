from flask import Flask, render_template, jsonify
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguestandings
import pandas as pd
from math import floor
import os

# Initialize Flask app
app = Flask(__name__)

# Load over/under data (cleaned earlier)
over_under_data = pd.read_excel('OU_Picks.xlsx', sheet_name='Sheet1', skiprows=4)
over_under_data.columns = ['Team', 'O/U', 'MT Picks', 'CH Picks', 'RT Picks']
over_under_data = over_under_data.dropna(subset=['Team']).reset_index(drop=True)

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