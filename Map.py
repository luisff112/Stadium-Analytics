import streamlit
import streamlit as st
import numpy as np
import pandas as pd
import re
import pydeck as pdk

df = pd.read_csv("stadiums-geocoded.csv") #decided not to add index_col
def remove_char(string):
    return re.sub(r'[^a-zA-Z0-9\s]', '', string) #searches any string that isnt upper/lower case, number, space and replaces with empty string


df['stadium'] = df['stadium'].apply(remove_char) #apply function
df['team'] = df['team'].apply(remove_char)
#dictionary w all acronyms
statesdic = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "Washington D.C.": "DC",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

#change all states to acronyms, also get D.C. to work
def state_prob(state):
    state = state.strip()
    state = state.replace('.','')
    if len(state) == 2:
        return state
    else:
        try:
            return statesdic[state]
        except KeyError:
            return 'N/A'
df['state'] = df['state'].apply(state_prob) #changing states

#function to get expanded column clear with no issues
def yearfunc(yr):
    if pd.isnull(yr):
        return np.nan
    elif len(yr) >= 4:
        return yr[:4]
    else:
        return np.nan

df['expanded'] = df['expanded'].apply(yearfunc)

#Finished clearing all errors in data

Locations = [(state, lat, long, team, stadium) for state, lat, long, team, stadium in zip(df['state'], df['latitude'], df['longitude'], df['team'], df['stadium'])] #creates a tuple


gp = pd.DataFrame(Locations, columns=["state", "lat", "lon", "team","stadium"])


view_state = pdk.ViewState(
    latitude=gp["lat"].mean(),
    longitude=gp["lon"].mean(),
    zoom = 5,
    pitch = 100)

# a scatterplot layer
layer1 = pdk.Layer('ScatterplotLayer',
                  data = gp,
                  get_position = '[lon, lat]',
                  get_radius = 10000,
                  get_color = [0,0,255],
                  pickable = True)
st.title("Stadiums around United States")
tool_tip = {"html": "<b>Name: {stadium}</b><br><b>State: {state}</b><br><b>Team: {team}</b>",
            "style": { "backgroundColor": "lightblue",
                        "color": "black"}}

map = pdk.Deck(
    map_style='mapbox://styles/mapbox/satellite-streets-v12',
    initial_view_state=view_state,
    layers=[layer1],
    tooltip= tool_tip
)

st.pydeck_chart(map)
st.write("On this Map we can see many blue dots around the whole United States, which helps see better where are more stadiums and if looking to see one which one could be the closest to you")

