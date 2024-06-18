import os
import json
import pandas as pd
import streamlit as st

from mplsoccer import VerticalPitch, Pitch


def scrape_sofascore(url: str) -> None:

    match_id = url.split('#id:')[-1]

    shots_response = json.loads(os.popen(
        f'curl -H "Host: api.sofascore.com" -H "Accept: */*" -H "User-Agent: curl/8.1.2" https://api.sofascore.com/api/v1/event/{match_id}/shotmap'
    ).read())['shotmap']

    home_shots = pd.DataFrame([x for x in shots_response if x['isHome']])
    away_shots = pd.DataFrame([x for x in shots_response if not x['isHome']])

    event_info = json.loads(os.popen(
        f'curl -H "Host: api.sofascore.com" -H "Accept: */*" -H "User-Agent: curl/8.1.2" https://api.sofascore.com/api/v1/event/{match_id}'
    ).read())['event']

    home_team_name = event_info['homeTeam']['name']
    away_team_name = event_info['awayTeam']['name']

    df = pd.concat([home_shots, away_shots])

    # Add team name to the dataframe
    df['team'] = df['isHome'].apply(lambda x: home_team_name if x else away_team_name)
    df['player'] = df['player'].apply(lambda x: x['name'])
    df['x'] = df['playerCoordinates'].apply(lambda x: x['x'])
    df['y'] = df['playerCoordinates'].apply(lambda x: x['y'])

    df = df[[
        'id', 'team', 'player', 'x', 'y', 'xg', 'xgot', 'shotType', 'situation'
    ]]

    # Append the data to the shots.csv
    df.to_csv('~/Documents/Github/streamlit/streamlit_euros/shots.csv', mode='a', header=False, index=False)


# scrape_sofascore('https://www.sofascore.com/germany-scotland/VTbslUb#id:11873905')
# scrape_sofascore('https://www.sofascore.com/hungary-switzerland/ZTbsjUb#id:11873897')
# scrape_sofascore('https://www.sofascore.com/croatia-spain/YTbspUb#id:11873907')
# scrape_sofascore('https://www.sofascore.com/italy-albania/PTbshUb#id:11873898')
# scrape_sofascore('https://www.sofascore.com/netherlands-poland/dUbsfUb#id:12198302')
# scrape_sofascore(url='https://www.sofascore.com/slovenia-denmark/BObsJOb#id:11873971')
# scrape_sofascore('https://www.sofascore.com/serbia-england/nUbsfCc#id:11873969')
# scrape_sofascore('https://www.sofascore.com/austria-france/GObstUb#id:11873975')
# scrape_sofascore('https://www.sofascore.com/ukraine-romania/CObsbUb#id:12198226')
# scrape_sofascore('https://www.sofascore.com/belgium-slovakia/XTbsrUb#id:11873978')
scrape_sofascore('https://www.sofascore.com/georgia-turkey/aUbsnVb#id:12198159')
scrape_sofascore('https://www.sofascore.com/czech-republic-portugal/eUbsoUb#id:11873989')


st.title("Euros 2024 Shot Map")
st.subheader("Filter to any team/player to see all their shots taken!")

# Load the data
try:
    df = pd.read_csv('./streamlit_euros/shots.csv')
    # df = pd.read_csv('~/Documents/Github/streamlit/streamlit_euros/shots.csv')
    df = df[df['situation'] != 'own'].reset_index()
    df = df.sort_values(by=['team', 'player'])
except pd.errors.EmptyDataError:
    st.error("The data file is empty or not found.")
    st.stop()

# Ensure there is a valid default selection
if df.empty:
    st.error("No data available to display.")
    st.stop()


def filter_data(df: pd.DataFrame, team: str, player: str):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df


def plot_shots(df, ax, pitch):
    ax.set_title("Shot Map")
    if not df.empty:
        for x in df.to_dict(orient='records'):
            pitch.scatter(
                x=100 - x['x'],
                y=100 - x['y'],
                ax=ax,
                s=1000 * x['xg'],
                color='green' if x['shotType'] == 'goal' else 'white',
                edgecolors='black',
                alpha=1 if x['shotType'] == 'goal' else .5,
                zorder=2 if x['shotType'] == 'goal' else 1
            )

# Selectbox with a default selection that exists
team = st.selectbox("Select a team", df['team'].unique(), index=0)
player = st.selectbox("Select a player", df[df['team'] == team]['player'].unique(), index=None)
filtered_df = filter_data(df, team, player)

# Create a pitch
pitch = VerticalPitch(pitch_type='opta', line_zorder=2, pitch_color='#f0f0f0', line_color='black', half=True)
fig, ax = pitch.draw(figsize=(10, 10))
plot_shots(filtered_df, ax, pitch)

st.pyplot(fig)


st.text("Last Updated: 2024-06-18")
