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

from Recuperation_dataverses import Recup_dataverses, Recup_contenu_dataverse, Recup_contenu_dataset,Recup_contenu

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

########### COULEURS SIDEBAR ######################################
st.markdown("""
 <style>
    [data-testid=stSidebar] {
        background-color: rgb(6,51,87,0.2);
    }
    .st-emotion-cache-1dj0hjr {
            color: #3b979f;
    }
    .st-emotion-cache-1rtdyuf {
            color: #3b979f;
    }
    .st-emotion-cache-6tkfeg {
            color: #3b979f;
    }
    .st-emotion-cache-1q2d4ya {
            color: #3b979f;
    }
    </style>
""", unsafe_allow_html=True)

##########################  VARIABLES DE CONNEXION #######################
BASE_URL="https://data.indores.fr"
API_TOKEN="19f0769d-564f-44ac-809b-22853f186960"
##########################################################################
st.title(":grey[Analyse des dépôts dans Data.InDoRes]")

adresse_dataInDoRes = 'https://data.indores.fr/dataverse/dataindores'
s_adresse_dataInDoRes = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_dataInDoRes}</p>"
st.markdown(s_adresse_dataInDoRes ,unsafe_allow_html=True)

###################### CREATION CONNEXION ##############################

def connect_to_dataverse(BASE_URL, API_TOKEN):
    try:
        # Create a new API connection
        api = NativeApi(BASE_URL, API_TOKEN)
        resp = api.get_info_version()
        response = resp.json()
        
        # Check connection success
        if response['status']=='OK':
            st.session_state['dataverse_api'] = api
            st.success("Connexion établie avec Data. InDoRES")
        else:
            st.error("Connexion échouée!")
    except Exception as e:
        st.error(f"Connection error: {e}")
    return api


# Initialize session state if not already done
if 'dataverse_api' not in st.session_state:
    st.session_state['dataverse_api'] = None

Connexion_dataInDoRES = st.sidebar.button('Se connecter à Data.InDoRES')
# Button to trigger connection
if Connexion_dataInDoRES:
    with st.spinner("Connexion au Dataverse Data.InDoRes en cours"):
        api = connect_to_dataverse(BASE_URL,  API_TOKEN)
    
# Display connection status
if st.session_state['dataverse_api'] is not None:
    st.write("Vous êtes connectés à Data.InDoRES")


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
graph_title_font = 24
graph_xaxis_ticks_font = 15
graph_xaxis_title_font = 20
graph_yaxis_ticks_font = 15
graph_yaxis_title_font = 20
legend_title_font = 15
legend_font =15
graph_title_color = "gray"
graph_ticks_color = 'gray'

############################################################################

fi = glob.glob(f"pages/data/tableau_dataverses*.csv")

############################################################################

all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)


def find_indices(lst, elements):
    indices = []
    for element in elements:
        try:
            indices.append(lst.index(element))
        except ValueError:
            pass  # Element not found in the list
    return indices

ids = find_indices(liste_ZAs_, Selection_ZA)

###############################################################################################
########### POUR L'ADMINISTRATEUR ############################################################
###############################################################################################

# Mot de passe pour faire des récupérations automatisées
admin_pass = 'admin'
admin_action = st.sidebar.text_input(label="Pour l'administrateur")


if admin_action == admin_pass:

    # MAJ DES ENTREPOTS EXISTANTS ##########################################
    b1 = st.sidebar.button(label=" Mise à jour des entrepôts Dataverses dans Data.InDoRes ")

    if b1==True:
        with st.spinner("Récupération des entrepôts existants"):
            Recup_dataverses(api,fichier)


    # RECUPERATION DES CONTENUS VIA BOUTON ##########################################       
    Recup_globale = st.sidebar.button('recupération des contenus')
    if Recup_globale:
        with st.spinner("La récup globale est en cours"):
            liste_columns_df_entrepot=['selection','Entrepot','ID','Url','Date de publication','Titre','Auteur','Organisation',"Email",'Résumé','Thème','Publication URL']
            df_entrepot = pd.DataFrame(columns=liste_columns_df_entrepot)
            for i, za in enumerate(Selection_ZA):
                s = liste_ZAs_bis[ids[i]][1]
                df = Recup_contenu(api, s, za)
                dfi = pd.concat([df_entrepot,df], axis=0)
                dfi.reset_index(inplace=True)
                dfi.drop(columns='index', inplace=True)
                df_entrepot = dfi
            df_entrepot.to_csv("pages/data/Contenu_DataInDoRES2.csv")

############################################################################

df_complet = pd.read_csv("pages/data/Contenu_DataInDoRES2.csv",index_col=[0])

if len(Selection_ZA)!=0:
    
    with st.container(border=True):
        Nombre_depots = df_complet['Entrepot'].value_counts()
        for i in range(len(liste_ZAs_)):
            if liste_ZAs_[i] in Nombre_depots.index.values:
                pass
            else:
                Nombre_depots[liste_ZAs_[i]]=0
        df = pd.DataFrame(Nombre_depots.values,index=Nombre_depots.index.values,columns=['Nombre_dépôts'])
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
                                    font=dict(size=graph_title_font, family='Arial', color=graph_title_color)
                                ),
                                yaxis=dict(
                                    tickfont=dict(size=graph_yaxis_ticks_font, family='Arial', color=graph_ticks_color)   
                                ),
                                xaxis=dict(
                                    tickfont=dict(size=graph_xaxis_ticks_font, family='Arial', color=graph_ticks_color)   
                                ),
                                width=1000,
                                height=600,
                                showlegend=False)
        st.plotly_chart(fig0,use_container_width=True)

    with st.container(border=True):
        st.dataframe(df_complet[df_complet['ZA'].isin(Selection_ZA)])

#############  VISU SUNBURST ###############################################

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

##########POUR L'ADMINISTRATEUR ########################################



############################################################################