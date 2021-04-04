import pandas as pd

import numpy as np
import datetime
import wget
from pathlib import Path
"""         
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
* [Deploy PyCaret and Streamlit app using AWS Fargate — serverless infrastructure](https://towardsdatascience.com/deploy-pycaret-and-streamlit-app-using-aws-fargate-serverless-infrastructure-8b7d7c0584c2)
* [Turn your Jupyter Notebooks into a web app using Streamlit](https://medium.com/@shalinisinghzoots/turn-your-jupyter-notebooks-into-a-web-app-using-streamlit-414b76f1e094)
* [How to build interactive dashboards in Python using Streamlit](https://towardsdatascience.com/how-to-build-interactive-dashboards-in-python-using-streamlit-1198d4f7061b)
* [Web app for Interactive data exploration using Streamlit (fastest way to build Machine learning tools)](https://medium.com/analytics-vidhya/web-app-for-interactive-data-exploration-usig-streamlit-fastest-way-to-build-machine-learning-563783aa0a81)
* [COVID-19 Dashboard in Python using Streamlit](https://medium.com/analytics-vidhya/covid-19-dashboard-in-python-using-streamlit-aa58581e5a7f)
* [API Vzla](https://covid19.patria.org.ve/api-covid-19-venezuela/)
* [Streamlit 101: An in-depth introduction](https://towardsdatascience.com/streamlit-101-an-in-depth-introduction-fc8aad9492f2)
* [Streamlit](https://docs.streamlit.io/en/stable/api.html)
"""

path = "./covid19/csse_covid_19_data/csse_covid_19_daily_reports/"


def ls3(path):
    """
    Retorna una lista de archivos de una ruta (path) dada.
    :param path: Ruta del directorio donde se encuentran los archivos a listar
    :return filenames 
    """
    return [obj.name for obj in Path(path).iterdir() if obj.is_file()]


def getData(country="Venezuela", date="03-13-2020", path=path, encoding="ISO-8859-1"):
    """
    Obtiene los datos desde una fecha y para un país, de la ruta definida de archivos csv.
    :param country: País que se quiere generar el dataframe
    :param date: Fecha desde que se va a tomar los datos para el dataframe
    :param path: Ruta donde se encuentran los archivos csv
    :param encoding: Codificación a la que se encuentran los archivos csv.
    :return df: Dataframe con los datos extraídos de los csv desde una fecha dada y para un país.
    """
    # Se obtiene los nombres de los archivos.
    lista = [file for file in ls3(path) if file.split(".")[-1] == "csv"]
    # Se lee los archivos csv y se convierten en varios dataframe en un diccionario ordenados por fecha.
    df = {item.split(".")[0]: pd.read_csv(
        path + "/" + item, encoding=encoding) for item in lista}
    # Se lista las fechas
    dates = [item.split(".")[0] for item in lista]
    # Se renombras las columnas de los dataframes.
    for i, date in enumerate(dates):
        if "Country_Region" in list(df[date].columns) or "Province_State" in list(df[date].columns) or "Last_Update" in list(df[date].columns):
            df[date].rename(columns={"Country_Region": 'Country/Region',
                                     "Last_Update": "Last Update", "Province_State": "Province/State"}, inplace=True)
    # Se convierten las fechas en datetime y se ordenan
    dates2 = sorted([datetime.datetime.strptime(date, "%m-%d-%Y")
                     for date in dates])
    # Se ordena los dataframes en una lista
    if country != None:
        data = [df[d.strftime("%m-%d-%Y")][df[d.strftime("%m-%d-%Y")]["Country/Region"] == country]
                for d in dates2 if d >= datetime.datetime.strptime(date, "%m-%d-%Y")]
    else:
        data = [df[d.strftime("%m-%d-%Y")] for d in dates2 if d >=
                datetime.datetime.strptime(date, "%m-%d-%Y")]

    # Se concatena los dataframes en uno sólo y se retorna
    data_df = pd.concat(data)
    return data_df


def AddColumnRate(df, column_name):
    """
    Agrega una columna al dataframe, dicha columna es la diferencia entre la próxima row y el row actual
    :param df: DataFrame a agregar la columna.
    :param column_name: Columna a la que se quiere calcular la diferencia.
    :return df: Retorna un dataframe con la columna adicional que tiene la diferencia por día.
    """
    elements = []
    # Se recorre el dataframe
    for i in range(len(df)):
        # Si es la fila inicial se toma su valor
        if i == 0:
            elements.append(df.iloc[0][column_name])
        else:
            # Si no es el inicial se calcula la diferencia de su valor actual con el anterior
            elements.append(df.iloc[i][column_name] -
                            df.iloc[i-1][column_name])
    # Se agrega la lista al dataframe
    df.insert(4, f"rate_{column_name}", elements)
    return df


def DataProcessor(df):
    """
    Se remueve columnas del dataframe, se define el index, se reemplaza los NA y se agrega dos columnas.
    :param df: Dataframe a procesar
    :return df: DataFrame procesado
    """
    # Se obtiene el nombre de una columna a remover
    remove = list(df.columns)[0]
    print(list(df.columns))
    # Se remueve la lista de columnas
    df.drop(labels=["Province/State", "Admin2",
                    "Lat", "Long_", "Combined_Key", "FIPS", remove], axis=1, inplace=True)
    df.drop(labels=[df.columns[-2]], axis=1, inplace=True)
    # Se reemplaza NA por 0.
    df.fillna(0, inplace=True)
    # Se conviernte las fechas que son string a datetime
    df['Last Update'] = pd.to_datetime(df['Last Update'])
    # Se define las fechas como indice
    df.set_index("Last Update", inplace=True)
    # Se calcula los rate de confirmados y muertes
    return df


def GetCSV(url, filepath):
    wget.download(url, filepath)
    return pd.read_csv(filepath)
