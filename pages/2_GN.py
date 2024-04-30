import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.options.mode.chained_assignment = None

st.title("Analyse des catalogues")

liste_ZAs= ['ZA1','ZA2','ZA3']
Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs)

##################################### LECTURE DATA ###########################################
data = pd.read_csv("data\Enregistrements_190424.csv")

##################################### TRAITEMENT PREALABLE ###################################
data_dates=data[["createDate"]]
data_dates.rename(columns={"createDate":"Date"}, inplace=True)
nb_enregistrements = len(data_dates)
data_dates.dropna(subset="Date" ,inplace=True)
data_dates['Date'] = pd.to_datetime(data_dates['Date'], format='mixed', utc=True)
data_dates.sort_values(by="Date", inplace=True)
data_dates.loc[:,'Compte']=np.arange(len(data_dates))+1
data_dates.set_index('Date', inplace=True)

#st.scatter_chart(data=data_dates, x='Date', y='compte')

###################################### VISUALISATION #########################################
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=data_dates.index, y=data_dates['Compte'], name="Cumul d'enregistrements"),secondary_y=False)
fig.update_layout(title_text=f"évolution temporelle des enregistrements", font_size = 20, showlegend=False)
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Nombre cumulé d'enregistrements",title_font=dict(color='Black'),secondary_y=False)
#fig.update_yaxes(title_text="Nombre d'enregistrements",title_font=dict(color='red'),secondary_y=True)
st.plotly_chart(fig)
