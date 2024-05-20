import streamlit as st
import pandas as pd
import requests
import json
import os.path
from os import path
import re
import numpy as np
import datetime
import plotly.express as px

from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Analyse des Dataverses",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

##########################  VARIABLES DE CONNEXION #######################
BASE_URL="https://data.indores.fr"
API_TOKEN="19f0769d-564f-44ac-809b-22853f186960"
##########################################################################

###################### CREATION CONNEXION ##############################
with st.spinner("Connexion au Dataverse Data.InDoRes en cours"):
    api = NativeApi(BASE_URL, API_TOKEN)
    resp = api.get_info_version()
    response = resp.json()

col1, col2 = st.columns(2)
with col1:
    d = datetime.date.today()
    if response['status']=='OK':
        st.write(f"La connexion est établie avec Data.InDoRes")
    else: 
        st.write(f"La connexion a échoué, vous n'êtes pas connecté à Data.InDoRes")

with col2:
    b1 = st.button(label=" Mise à jour des entrepôts Dataverses dans Data.InDoRes ")

fichier = f'tableau_dataverses-{d}.csv'
if b1==True:
    with st.spinner("Récupération des entrepôts existants"):
        if path.exists(f"pages/data/{fichier}"):
            test = pd.read_csv(f"pages/data/{fichier}")

            fig = px.sunburst(test, path=['niv0','niv1', 'niv2'], values='val')
            st.plotly_chart(fig,use_container_width=True)
        else:
            # On peut aller chercher le contenu du dataverse
            # le status est rappelé puis on a une clé "data" dans laquelle on retrouve son contenu.
            # Pour dataindores: d'autres sous-dataverses!
            dataindores = api.get_dataverse_contents("dataindores")
            data_indores = dataindores.json()
            # Ici on récupère les noms de ces dataverses et les id 
            # On crée un premier tableau avec ces élements
            liste_dataverses_1= []
            liste_ids = []
            for d in range(len(data_indores['data'])):
                if data_indores['data'][d]['type']=="dataverse":
                    liste_dataverses_1.append(data_indores['data'][d]['title'])
                    liste_ids.append(data_indores['data'][d]['id'])
            df_liste_dataverses_1=pd.DataFrame(data=[liste_dataverses_1,liste_ids], index=['Dataverses_niv1','Ids'])
            df_liste_dataverses_1=df_liste_dataverses_1.T
            # A partir de ce tableau, pour chacun des dataverses répertoriés (niv1), on récupère les noms des sous-dataverses (niv2) 
            # On enregistre ces infos dans un csv
            liste = []
            ids = []
            for i in range(len(df_liste_dataverses_1)):
                datav = api.get_dataverse_contents(df_liste_dataverses_1.loc[i,'Ids'])
                datav_dv = datav.json()
                liste_dataverses_2 = []
                ids_niv2 = []
                for d in range(len(datav_dv['data'])):
                    try:
                        if datav_dv['data'][d]['type']=="dataverse":
                            liste_dataverses_2.append(datav_dv['data'][d]['title'])
                            ids_niv2.append(datav_dv['data'][d]['id'])
                    except:
                            liste_dataverses_2.append()
                            ids_niv2.append()
                liste.append(liste_dataverses_2)
                ids.append(ids_niv2)
            
            df_liste_dataverses_1['Dataverses_niv2']=liste
            df_liste_dataverses_1['Ids_niv2']=ids
            df_liste_dataverses_1.to_csv(f"pages/data/liste_dataverses.csv")

            data = pd.read_csv(f"pages/data/liste_dataverses.csv")
            data.drop(columns=['Unnamed: 0'], inplace=True)
            for i in range(len(data)):
                    data.loc[i,'val']=int(len(re.split(',',data.loc[i,'Dataverses_niv2'].replace('[','').replace(']','').replace("'",''))))

            som = sum(data['val'].values)
            new_data = pd.DataFrame(index=np.arange(0,som), columns=['niv1','niv2'])
            i=0
            for j in range(len(data)):
                for k in range(int(data.loc[j,'val'])):
                    new_data.loc[i,'niv1']=data.loc[j,'Dataverses_niv1']
                    new_data.loc[i,'ids_niv1']=data.loc[j,'Ids']
                    new_data.loc[i,'niv2']=re.split(',',data.loc[j,'Dataverses_niv2'].replace('[','').replace(']','').replace("'",''))[k]
                    new_data.loc[i,'ids_niv2']=re.split(',',data.loc[j,'Ids_niv2'].replace('[','').replace(']','').replace("'",''))[k]
                    i+=1
            new_data['val']=1
            new_data['niv0']="Data_InDoRes"
            new_data.to_csv(f"pages/data/{fichier}")
            fig = px.sunburst(new_data, path=['niv0','niv1', 'niv2'], values='val')
            st.plotly_chart(fig,use_container_width=True)
else:
    new_data = pd.read_csv(f"pages/data/{fichier}")
    new_data.drop(columns=['Unnamed: 0'], inplace=True)
    fig = px.sunburst(new_data, path=['niv0','niv1', 'niv2'], values='val')
    fig.update_layout(
                title='Visuel des différents Dataverses dans Data.InDoRes',
                width=1000,
                height=1000)
    st.plotly_chart(fig,use_container_width=True)


st.title("Analyse des entrepôts")
liste_ZAs= ['ZAA','ZA2','ZA3']
Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs)

with st.container(border=True):
    row1 = st.columns(2)

    with row1[0]:
        st.write('à remplir')
    with row1[1]:
        st.write('à remplir')

with st.container(border=True):
    row2 = st.columns(2)

    with row2[0]:
        st.write('à remplir')
    with row2[1]:
        st.write('à remplir')