import streamlit as st
import plotly.express as px
import pydeck as pdk
import pandas as pd 
import datetime

import wget 
import os
from getdata import getData,DataProcessor,GetCSV

now = datetime.datetime.now()

datenow = now.strftime("%d-%m-%Y")

path = "/home/ernesto/proyectos/streamlit-covid-19-vzla/covid19/csse_covid_19_data/csse_covid_19_daily_reports/"
directory = "./data/"

start = "01-01-2020"
df = getData(country=None,date=start)
df = DataProcessor(df)

df.drop(columns=[list(df.columns)[4]],inplace=True)
countries = sorted(list(set(df["Country/Region"])))
select_graph = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'Case-Fatality_Ratio']

selects = []

st.sidebar.header('Covid-19')

st.title(f" Covid-19 data Venezuela" )
st.write(df[df["Country/Region"] == "Venezuela"][select_graph].tail(1))
st.write(f"## Venezuela")

st.line_chart(df[df["Country/Region"] == "Venezuela"][select_graph])


st.write("## States of Venezuela")    
url1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQI4s0no2TS1dYxbv82nhKD7iz8fbDGwdsOI4kzJ0cg3gjOR51KIw_rNOff97Xic_fRQD41xmsDGUfM/pub?gid=1029482781&single=true&output=csv"

filename1 = f"bystate_historic_{datenow}.csv"
filepath1 = directory + filename1

if os.path.exists(filepath1):
    bystate = pd.read_csv(filepath1)
else:
    bystate = GetCSV(url1,filepath1)


bystate["date"] = pd.to_datetime(bystate["date"])
bystate.set_index("date",inplace=True)
states = sorted(list(bystate.columns))
    
    
st.line_chart(bystate)
option_state = st.sidebar.selectbox('States:',states)
st.write(f"## Cases confirmed in {option_state}")
st.write(bystate[option_state].tail(1))
st.line_chart(bystate[option_state])

url2 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTT8ef-uVa5q_5kBYbVXeEpRCW8gOJHlWhHGrH8dQ704D64_yNaMMjvkzdgD9YweSBQ-GyqnGLLasvK/pub?gid=1574343536&single=true&output=csv"
filename2 = f"Covid-19 confirmed cases by age and gender_{datenow}.csv"
filepath2 = directory + filename2
if os.path.exists(filepath2):
    elements = []
    for item in pd.read_csv(filepath2).columns:
        elements.append(str(item))
    
    cols = [item for item in elements]
    
    ageandgender = pd.read_csv(filepath2,skiprows=2,names=cols) 
else:
    wget.download(url2,filepath2)
    elements = []
    for item in pd.read_csv(filepath2).columns:
        elements.append(str(item))
    
    cols = [item for item in elements]
    
    ageandgender = pd.read_csv(filepath2,skiprows=2,names=cols)

            
df1 = ageandgender.transpose()
df1 
    
st.sidebar.markdown("""
        ### Data sources: 
        
        * [OCHA](https://data.humdata.org/dataset/5f6fbd24-5266-42b7-82e9-70dd1e33a280)
        
        ### References: 
        * [docs streamlit.io](https://docs.streamlit.io/en/stable/getting_started.html#draw-charts-and-maps)
        * [Streamlit 101: An in-depth introduction](https://towardsdatascience.com/streamlit-101-an-in-depth-introduction-fc8aad9492f2)
        * [Learn How to Create Web Data Apps in Python](https://towardsdatascience.com/learn-how-to-create-web-data-apps-in-python-b50b624f4a0e)
        * [Build and deploy machine learning web app using PyCaret and Streamlit](https://towardsdatascience.com/build-and-deploy-machine-learning-web-app-using-pycaret-and-streamlit-28883a569104)
        * [Deploying ML web apps with Streamlit, Docker and AWS](https://medium.com/usf-msds/deploying-web-app-with-streamlit-docker-and-aws-72b0d4dbcf77)
        * [How to Deploy a Streamlit App using an Amazon Free ec2 instance?](https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3)
        * [How to Create Interactive Visualisations in Python](https://towardsdatascience.com/how-to-create-interactive-visualisations-in-python-4af42cf83ba4)
        * [spacy-streamlit](https://github.com/explosion/spacy-streamlit)
        * [Chanin Nantasenamat ](https://github.com/dataprofessor/code/blob/master/streamlit/part3/penguins-app.py)
    """)