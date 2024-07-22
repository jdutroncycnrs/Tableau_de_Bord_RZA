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

from Recuperation_dataverses import Recup_dataverses

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
liste_ZAs_ = [' Zone atelier Alpes',' Zone atelier arc jurassien',' Zone atelier Armorique',' Zone atelier environnementale urbaine',' Zone atelier bassin du Rhône',' Zone atelier Brest Iroise',' Zone atelier bassin de la Moselle',' Zone atelier Loire',' Zone Atelier Seine',' Zone atelier Pyrénées Garonne','Zone atelier territoires uranifères',' Zone atelier Plaine et Val de Sèvre',' Zone atelier Hwange','Zone atelier Environnementale Rurale','Zone atelier Santé Environnement Camargue','Zone atelier Antarctique et terres Australes']
colors = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0','#F9A2BF','#3E9399','#3D4A81','#ECDCC5','#D2CFC8','grey','grey','grey']
colors2 = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0','#F9A2BF','#3E9399','#3D4A81','grey','grey','grey']

############################################################################

fi = glob.glob(f"pages/data/tableau_dataverses*.csv")

visu_sunburst= st.sidebar.checkbox("Voir l'ensemble des entrepôts existants")

if len(fi)!=0:
    fich = fi[-1]
    data = pd.read_csv(fich)
    if visu_sunburst:
        fig = px.sunburst(data, path=['niv0','niv1', 'niv2','niv3'], values='val')
        fig.update_layout(
            title=f'Visuel des différents Dataverses dans Data.InDoRes via {fich}',
            width=1000,
            height=1000)
        st.plotly_chart(fig,use_container_width=True)
else:
     st.write('Il est nécessaire de mettre à jour vos entrepôts')

############################################################################

st.title("Analyse des entrepôts")

all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)

############################################################################

if len(Selection_ZA)!=0:
    with st.container(border=True):
        pass


##########POUR L'ADMINISTRATEUR ########################################

admin_pass = 'admin'
admin_action = st.sidebar.text_input(label="Pour l'administrateur")

if admin_action == admin_pass:
    b1 = st.sidebar.button(label=" Mise à jour des entrepôts Dataverses dans Data.InDoRes ")

    if b1==True:
        with st.spinner("Récupération des entrepôts existants"):
            Recup_dataverses(api,fichier)


############################################################################