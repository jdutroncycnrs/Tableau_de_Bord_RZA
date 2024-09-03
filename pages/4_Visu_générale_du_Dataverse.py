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
import plotly.graph_objects as go
import glob
import time

from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi

from Recuperation_dataverses import Recup_dataverses, Recup_contenu_dataverse

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

if response['status']=='OK':
    st.write(f"La connexion est établie avec Data.InDoRes")
else: 
    st.write(f"La connexion a échoué, vous n'êtes pas connecté à Data.InDoRes")

######################  PARAMETRES  #######################################

d = datetime.date.today()

fichier = f'tableau_dataverses-{d}.csv'

liste_ZAs= ['ZAA','ZAAJ','ZAAR','ZAEU','ZABR','ZABRI','ZAM','ZAL','ZAS','ZAPygar','ZATU','ZAPVS','ZAH','ZARG','ZACAM','ZATA']

liste_ZAs_ = ['Zone atelier territoires uranifères',
              ' Zone Atelier Seine',
              ' Zone atelier Loire',
              ' Zone atelier bassin du Rhône',
              ' Zone atelier bassin de la Moselle',
              ' Zone atelier Alpes',
              ' Zone atelier arc jurassien',
              ' Zone atelier Armorique',
              ' Zone atelier Plaine et Val de Sèvre',
              ' Zone atelier environnementale urbaine',
              ' Zone atelier Hwange',
              ' Zone atelier Pyrénées Garonne',
              ' Zone atelier Brest Iroise',
              ' Zone Atelier Antarctique et Terres Australes',
              ' Zone Atelier Santé Environnement Camargue',
              ' Zone Atelier Argonne']

liste_ZAs_bis = [['Zone atelier territoires uranifères','36'],
              [' Zone Atelier Seine','37'],
              [' Zone atelier Loire','38'],
              [' Zone atelier bassin du Rhône','39'],
              [' Zone atelier bassin de la Moselle','40'],
              [' Zone atelier Alpes','42'],
              [' Zone atelier arc jurassien','43'],
              [' Zone atelier Armorique','44'],
              [' Zone atelier Plaine et Val de Sèvre','45'],
              [' Zone atelier environnementale urbaine','46'],
              [' Zone atelier Hwange','47'],
              [' Zone atelier Pyrénées Garonne','48'],
              [' Zone atelier Brest Iroise','49'],
              [' Zone Atelier Antarctique et Terres Australes','10295'],
              [' Zone Atelier Santé Environnement Camargue','10296'],
              [' Zone Atelier Argonne','10297']]

colors = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0','#F9A2BF','#3E9399','#3D4A81','#ECDCC5','#D2CFC8','grey','grey','grey']

############################################################################

fi = glob.glob(f"pages/data/tableau_dataverses*.csv")

visu_sunburst= st.sidebar.checkbox("Voir l'ensemble des entrepôts existants")

if len(fi)!=0:
    fich = fi[-1]
    dataverses = pd.read_csv(fich)
    if visu_sunburst:
        fig = px.sunburst(dataverses, path=['niv0','niv1', 'niv2','niv3'], values='val')
        fig.update_layout(
            title=f'Visuel des différents Dataverses dans Data.InDoRes via {fich}',
            width=1000,
            height=1000)
        st.plotly_chart(fig,use_container_width=True)
else:
     st.write('Il est nécessaire de mettre à jour vos entrepôts')

############################################################################

st.title("Analyse des sous-entrepôts dans Data.InDoRes")

all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)

#Selected_dataverses = dataverses[['niv2','ids_niv2']][dataverses['niv2'].isin(Selection_ZA)]
#Selected_dataverses.reset_index(inplace=True)
#Selected_dataverses.drop(columns='index', inplace=True)
#Selected_dataverses['ids_niv2'] = Selected_dataverses['ids_niv2'].astype(str)

def find_indices(lst, elements):
    indices = []
    for element in elements:
        try:
            indices.append(lst.index(element))
        except ValueError:
            pass  # Element not found in the list
    return indices

ids = find_indices(liste_ZAs_, Selection_ZA)


############################################################################

if len(Selection_ZA)!=0:
    Nombre_depots = []
    with st.container(border=True):
        progress_text = "Operation en cours. Attendez svp."
        my_bar = st.progress(0, text=progress_text)
        for i in range(len(Selection_ZA)):
            time.sleep(0.1)
            try:
                s = liste_ZAs_bis[ids[i]][1]
                cpt = 0
                try:
                    datav_contenu = Recup_contenu_dataverse(api,s)
                    for j in range(len(datav_contenu['data'])):
                        try:
                            identifieur = datav_contenu["data"][j]['identifier']
                            cpt +=1
                        except:
                            pass
                except:
                    pass
            except:
                pass
            Nombre_depots.append(cpt)
            my_bar.progress(i + 1, text=progress_text)

        df = pd.DataFrame(Nombre_depots,index=Selection_ZA,columns=['Nombre_dépôts'])
        fig0= go.Figure()
        for i, za in enumerate(df.index.values):
            selec = df.index.values[i:i+1]
            selec_len = df['Nombre_dépôts'].values[i:i+1]
            fig0.add_trace(go.Bar(
                        y=selec,
                        x=selec_len,
                        name=za,
                        orientation = 'h',
                        marker=dict(color=colors[i])
                    ))
        fig0.update_layout(
                                title=dict(
                                    text=f'Nombre de dépôts répertoriées au {d}',
                                    font=dict(size=24, family='Arial', color='darkblue')
                                ),
                                yaxis=dict(
                                    tickfont=dict(size=20, family='Arial', color='black')     # Tick font
                                ),
                                xaxis=dict(
                                    tickfont=dict(size=20, family='Arial', color='black')     # Tick font
                                ),
                                width=1000,
                                height=600,
                                showlegend=False)
        st.plotly_chart(fig0,use_container_width=True)
        my_bar.empty()


##########POUR L'ADMINISTRATEUR ########################################

admin_pass = 'admin'
admin_action = st.sidebar.text_input(label="Pour l'administrateur")

if admin_action == admin_pass:
    b1 = st.sidebar.button(label=" Mise à jour des entrepôts Dataverses dans Data.InDoRes ")

    if b1==True:
        with st.spinner("Récupération des entrepôts existants"):
            Recup_dataverses(api,fichier)


############################################################################