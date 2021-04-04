import streamlit as st
import plotly.express as px
import pydeck as pdk
import pandas as pd
import datetime
import plotly.graph_objects as go


import wget
import os
from getdata.getdata import getData, DataProcessor, GetCSV
from constants import var

path = var["path"]

directory = var["directory"]
start = var["start"]
url1 = var["url1"]
url2 = var["url2"]


@st.cache(allow_output_mutation=True)
def getDF():
    df = getData(country=None, date=start)
    df = DataProcessor(df)
    df.drop(columns=[list(df.columns)[4]], inplace=True)
    return df


@st.cache(allow_output_mutation=True)
def getByState(datenow):
    filename1 = f"bystate_historic_{datenow}.csv"
    filepath1 = directory + filename1
    if os.path.exists(filepath1):
        bystate = pd.read_csv(filepath1)
    else:
        bystate = GetCSV(url1, filepath1)
    bystate["date"] = pd.to_datetime(bystate["date"])
    bystate.set_index("date", inplace=True)

    return bystate


@st.cache(allow_output_mutation=True)
def getByGender(datenow):
    filename2 = f"Covid-19 confirmed cases by age and gender_{datenow}.csv"
    filepath2 = directory + filename2
    if os.path.exists(filepath2):
        elements = []
        for item in pd.read_csv(filepath2).columns:
            elements.append(str(item))

        cols = [item for item in elements]

        ageandgender = pd.read_csv(filepath2, skiprows=2, names=cols)
    else:
        wget.download(url2, filepath2)
        elements = []
        for item in pd.read_csv(filepath2).columns:
            elements.append(str(item))

        cols = [item for item in elements]

        ageandgender = pd.read_csv(filepath2, skiprows=2, names=cols)

    return ageandgender


@st.cache(allow_output_mutation=True)
def ProssData(bystate):
    lastbystate = bystate.tail(1)
    lastbystate.reset_index(inplace=True)
    lastbystate.drop("date", axis=1, inplace=True)
    states = list(lastbystate.columns)
    values = list(dict(lastbystate.iloc[0]).values())
    data = pd.DataFrame({
        "index": states,
        "cases": values
    }).set_index('index')
    return data


def main():

    st.sidebar.header('Graphs:')
    select_graph = ["States", "State", "By Age", "By Gender"]
    selects = [item for item in select_graph if st.sidebar.checkbox(item)]
    now = datetime.datetime.now()
    datenow = now.strftime("%d-%m-%Y")
    df = getDF()
    countries = sorted(list(set(df["Country/Region"])))
    
    bystate = getByState(datenow)
    states = sorted(list(bystate.columns))
    ageandgender = getByGender(datenow)
    ages = ageandgender.drop(
        columns=['Confirmed Count', 'Confirmed Bygender Male', 'Confirmed Bygender Female'])
    agelabels = list(ages.columns)
    agevalues = list(ages.iloc[0])

    labels = ['Female', 'Male']
    male = int(ageandgender.iloc[0][['Confirmed Bygender Male']])

    female = int(ageandgender.iloc[0][['Confirmed Bygender Female']])
    values = [female, male]
    select_graph = ['Confirmed', 'Deaths',
                    'Recovered', 'Case_Fatality_Ratio']
    st.title(f" Covid-19 data Venezuela")
    
    st.write(df[df["Country/Region"] == "Venezuela"][select_graph].tail(1))
    st.write(f"## Venezuela")

    st.line_chart(df[df["Country/Region"] == "Venezuela"][select_graph])

    if "States" in selects:
        st.write("## States of Venezuela")
        data = ProssData(bystate)
        #st.dataframe(data)
        st.bar_chart(data)
        st.line_chart(bystate)

    if "States" in selects and "State" in selects:

        option_state = st.sidebar.selectbox('States:', states)
        st.write(f"## Cases confirmed in {option_state}")
        st.write(bystate[option_state].tail(1))
        st.line_chart(bystate[option_state])

    if "By Age" in selects:
        fig = go.Figure(data=[go.Pie(labels=agelabels, values=agevalues)])
        st.write("## By Age covid-19 confirmed")
        st.plotly_chart(fig)

    if "By Age" in selects and "By Gender" in selects:

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        st.write("## Gender covid-19 confirmed")
        st.plotly_chart(fig)

    st.sidebar.markdown("""
            ### Data sources: 
            
            * [OCHA (CSV)](https://data.humdata.org/dataset/5f6fbd24-5266-42b7-82e9-70dd1e33a280)
            * [Johns Hopkins Univerity (GitHub)](https://github.com/CSSEGISandData/COVID-19)    
    
        """)

    st.sidebar.info("""\
            
            by: [Ernesto Crespo](https://www.seraph.to/) | source: [GitHub](https://github.com/ecrespo/streamlit-covid-19-vzla) 
        """)


if __name__ == "__main__":
    main()
