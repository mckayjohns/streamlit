import os
import json
import pandas as pd
import streamlit as st

from mplsoccer import VerticalPitch


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
    df['xg'] = df['xg'].fillna(0)

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
# scrape_sofascore('https://www.sofascore.com/georgia-turkey/aUbsnVb#id:12198159')
# scrape_sofascore('https://www.sofascore.com/czech-republic-portugal/eUbsoUb#id:11873989')

# scrape_sofascore('https://www.sofascore.com/switzerland-scotland/VTbsZTb#id:11873903')
# scrape_sofascore('https://www.sofascore.com/germany-hungary/jUbslUb#id:11873900')
# scrape_sofascore('https://www.sofascore.com/croatia-albania/PTbspUb#id:11873906')
#
# scrape_sofascore('https://www.sofascore.com/serbia-slovenia/JObsfCc#id:11873974')
# scrape_sofascore('https://www.sofascore.com/england-denmark/BObsnUb#id:11873970')
# scrape_sofascore('https://www.sofascore.com/italy-spain/YTbshUb#id:11873901')

# scrape_sofascore('https://www.sofascore.com/ukraine-slovakia/XTbsbUb#id:12198231')
# scrape_sofascore('https://www.sofascore.com/austria-poland/dUbstUb#id:12198303')
# scrape_sofascore('https://www.sofascore.com/netherlands-france/GObsfUb#id:11873991')

# scrape_sofascore('https://www.sofascore.com/georgia-czech-republic/oUbsnVb#id:12198160')
# scrape_sofascore('https://www.sofascore.com/belgium-romania/CObsrUb#id:11873980')
# scrape_sofascore('https://www.sofascore.com/portugal-turkey/aUbseUb#id:11873984')

# scrape_sofascore('https://www.sofascore.com/hungary-scotland/VTbsjUb#id:11873899')
# scrape_sofascore('https://www.sofascore.com/germany-switzerland/ZTbslUb#id:11873902')
#
# scrape_sofascore('https://www.sofascore.com/spain-albania/PTbsYTb#id:11873904')
# scrape_sofascore('https://www.sofascore.com/croatia-italy/hUbspUb#id:11873896')

# scrape_sofascore('https://www.sofascore.com/serbia-denmark/BObsfCc#id:11873968')
# scrape_sofascore('https://www.sofascore.com/england-slovenia/JObsnUb#id:11873967')
# scrape_sofascore('https://www.sofascore.com/poland-france/GObsdUb#id:12198304')
# scrape_sofascore('https://www.sofascore.com/austria-netherlands/fUbstUb#id:11873977')
#
# scrape_sofascore('https://www.sofascore.com/slovakia-romania/CObsXTb#id:11873983')
# scrape_sofascore('https://www.sofascore.com/belgium-ukraine/bUbsrUb#id:12198234')
# scrape_sofascore('https://www.sofascore.com/czech-republic-turkey/aUbsoUb#id:11873986')
# scrape_sofascore('https://www.sofascore.com/georgia-portugal/eUbsnVb#id:12198161')

# scrape_sofascore('https://www.sofascore.com/italy-switzerland/ZTbshUb#id:11874022')
# scrape_sofascore('https://www.sofascore.com/germany-denmark/BObslUb#id:11874018')

# scrape_sofascore('https://www.sofascore.com/england-slovakia/XTbsnUb#id:11874017')
# scrape_sofascore('https://www.sofascore.com/georgia-spain/YTbsnVb#id:11874031')

# for x in [
#     'https://www.sofascore.com/belgium-france/GObsrUb#id:11874024',
#     'https://www.sofascore.com/portugal-slovenia/JObseUb#id:11874016',
#     'https://www.sofascore.com/netherlands-romania/CObsfUb#id:11874029',
#     'https://www.sofascore.com/austria-turkey/aUbstUb#id:11874025',
#     'https://www.sofascore.com/germany-spain/YTbslUb#id:11874027',
#     'https://www.sofascore.com/portugal-france/GObseUb#id:11874026'
#     'https://www.sofascore.com/england-switzerland/ZTbsnUb#id:11874019',
#     'https://www.sofascore.com/netherlands-turkey/aUbsfUb#id:11874021'
# ]:
#     scrape_sofascore(x)

st.title("Euros 2024 Shot Map")
st.subheader("Filter to any team/player to see all their shots taken!")

# Load the data
try:
    df = pd.read_csv('./streamlit_euros/shots.csv')
    df['xg'] = df['xg'].fillna(0)
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


st.text("Matches up to: 2024-07-06")
