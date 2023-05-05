import streamlit
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import squarify as sq
import random
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
graphss = ["Bar Chart", "Pie Chart", "TreeMap"]
st.sidebar.title("Choose graph")
selectting = st.sidebar.radio("Please select a graph to view:", graphss)
if selectting =="Bar Chart":
    st.title("Showing Bar Chart")
    st.bar_chart(df[['state', 'capacity']].set_index('state'))
    st.write("The graph shown here demonstrate which states currently has the highest capacity of people in which you can see how TN is ranking at the top almost with 800,000 capacity in all their stadiums while states like Washington (DC), Maine, wyoming are ranking at the lowest")
    avg = df['capacity'].mean()
    min = df['capacity'].min()
    max = df['capacity'].max()
    st.write("")
    st.write(f'The highest amount of capacity a state have is:  {format(max,",.0f")}')
    st.write(f'The smallest amount of capacity a state have is:  {format(min,",.0f")}')
    st.write(f'The average amount of capacity a state have is:  {format(avg,",.0f")}')
elif selectting == "Pie Chart":
    st.title("Showing Pie Chart")
    count = df['div'].value_counts()
    label = count.index.tolist() #creates list and respective counts
    amount = count.tolist() #counts

    fig, ax = plt.subplots()
    ax.pie(amount, labels=label, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal') #sets scaling to be equal
    st.pyplot(fig)
    st.write("From this graph we can tell how all stadiums in united states have only two div and they are pretty equal on amount of stadiums almost having a solid 50/50 ratio")

    count = df['conference'].value_counts()
    label = count.index.tolist() #creates list and respective counts
    amount = count.tolist() #counts

    fig, ax = plt.subplots(figsize=(10,10))
    plt.title("Stadiums distributed by conference")
    ax.pie(amount, autopct='%1.1f%%', startangle=90)
    ax.legend( label, title='Stadiums conference', loc='best', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True) #specifying pos of box, and graphics
    ax.axis('equal') #sets scaling to be equal
    st.pyplot(fig)

elif selectting == "TreeMap":
    st.title("Showing TreeMap")
    dt = df.groupby('state')['capacity'].sum().reset_index()

    labels = dt['state'].tolist()
    sizes = dt['capacity'].tolist()
    clist = []
    for i in range(len(labels)):
        r = lambda: random.randint(0, 255)
        color = '#%02X%02X%02X' % (r(), r(), r()) #generates random color. using rgb
        clist.append(color)

    # Creating the tree map
    plt.rc('font', size=12)
    sq.plot(sizes=sizes, label=labels, color=clist, alpha=0.7)
    plt.axis('off')
    st.pyplot()
    st.write("From this treemap we are able to see better how the capacity of each state is different and which states may have the highest capacity")

show10 = df.head(10)
st.dataframe(show10)
st.write("In this table we can we the top 10 stadiums in the list based on the data")