import streamlit
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re

#Name: Luis Quispe Tasayco
#CS230: Section 3
#Data: stadiums-geocoded

#Description:
#The program I have created today will demonstrate information about each museum and how they are located and related with their div,
#capacity, state. Also will be able to filter out some stadiums in order to find most convenient stadium to attend.
#(In order for the program to work correctly you must have the data on the pages file and the final project file)
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

#Website section
st.set_page_config(
    page_title="homepage"
) #Names the website

st.title("Stadium's data analysis")
st.subheader("CS230.3")
st.write("Welcome to my Data Analysis website, my name is Luis Quispe and the topic of this website is stadiums which we will be able to interact with graphs and maps ")
st.write("This website is designed to help you understand better each stadium located in the united states and choose which one can be bigger, smaller, different divs, and conference")
st.write("Any feedback is gladly appreciate it. If you have any, please make sure to leave your feedback on the comment section which I check on a daily baisis and will be able to implement new content or suggestions ")


feedback = st.text_input("Please leave feedback here: ")
if st.button("Submit Feedback"):
    with open("feedback", "a") as f:
        f.write(feedback + "\n")
        st.write("Thank you! I will read it soon")






#References:
#https://stackoverflow.com/     #just used this link since I  used stackoverflow in more than 2 scenarios
#https://gist.github.com/rogerallen/1583593
#https://www.youtube.com/watch?v=YClmpnpszq8
#https://realpython.com/
#Streamlitmap
#https://discuss.streamlit.io/   #Used more than twice

