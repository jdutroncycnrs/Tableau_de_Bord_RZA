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

# Paramètres visuels
couleur_subtitles = (250,150,150)
taille_subtitles = "25px"
couleur_subsubtitles = (60,150,160)
taille_subsubtitles = "25px"
couleur_True = (0,200,0)
couleur_False = (200,0,0)
wch_colour_box = (250,250,220)
wch_colour_font = (90,90,90)
fontsize = 70

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
            api = connect_to_dataverse(BASE_URL,  API_TOKEN)
            Recup_dataverses(api,fichier)


    # RECUPERATION DES CONTENUS VIA BOUTON ##########################################       
    Recup_globale = st.sidebar.button('recupération des contenus')
    if Recup_globale:
        with st.spinner("La récup globale est en cours"):
            api = connect_to_dataverse(BASE_URL,  API_TOKEN)
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
                                text=f'Nombre de dépôts répertoriées',
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

if len(Selection_ZA)!=0:
    df_visu = df_complet[df_complet['Entrepot'].isin(Selection_ZA)]
    df_visu.reset_index(inplace=True)
    df_visu.drop(columns='index', inplace=True)
    #st.dataframe(df_visu)

    if len(Selection_ZA)==1:
        col1,col2 = st.columns([0.7,0.3])
        with col1:
            Visu_depots = f"Données publiées dans la {Selection_ZA[0]}"
            s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
            st.markdown(s_Visu_depots ,unsafe_allow_html=True)
        with col2:
            st.metric(label="Nombre de dépôts décomptés", value=len(df_visu))
    elif 1<len(Selection_ZA)<16:
        col1,col2 = st.columns([0.7,0.3])
        with col1:
            Visu_depots = f"Données publiées dans les ZA suivantes: {Selection_ZA}"
            s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
            st.markdown(s_Visu_depots ,unsafe_allow_html=True)
        with col2:
            st.metric(label="Nombre de dépôts décomptés", value=len(df_visu))
    elif len(Selection_ZA)==16:
        col1,col2 = st.columns([0.7,0.3])
        with col1:
            Visu_depots = f"Données publiées dans l'ensemble du réseau des Zones Ateliers"
            s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
            st.markdown(s_Visu_depots ,unsafe_allow_html=True)
        with col2:
            st.metric(label="Nombre de dépôts décomptés", value=len(df_visu))
    
    if len(df_visu)!=0:
            for i in range(len(df_visu)):
                with st.container(border=True):
                    t0 = f"FICHIER #{i+1}"
                    s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                    st.markdown(s_t0,unsafe_allow_html=True)
                    col1,col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        t0a = 'Titre'
                        s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                        st.markdown(s_t0a,unsafe_allow_html=True)
                        st.markdown(df_visu.loc[i,'Titre'])
                    with col2:
                        t0b = 'Thème'
                        s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                        st.markdown(s_t0b,unsafe_allow_html=True)
                        st.markdown(df_visu.loc[i,'Thème'])
                    with col3:
                        t0c = 'Date'
                        s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                        st.markdown(s_t0c,unsafe_allow_html=True)
                        st.markdown(df_visu.loc[i,'Date de publication'])
                    col1,col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        t0d = 'Résumé'
                        s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                        st.markdown(s_t0d,unsafe_allow_html=True)
                        st.markdown(df_visu.loc[i,'Résumé'])
                    with col2:
                        t0e = 'Publication URL'
                        s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                        st.markdown(s_t0e,unsafe_allow_html=True)
                        st.markdown(df_visu.loc[i,'Publication URL'])
                    with col3:
                        t0f = 'DOI'
                        s_t0f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0f}</p>"
                        st.markdown(s_t0f,unsafe_allow_html=True)
                        st.markdown(df_visu.loc[i,'Url'])
                    col1,col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        t0g = 'Auteur'
                        s_t0g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0g}</p>"
                        st.markdown(s_t0g,unsafe_allow_html=True)
                        st.markdown(df_visu.loc[i,'Auteur'])
                    with col2:
                        t0h = 'Organisation'
                        s_t0h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0h}</p>"
                        st.markdown(s_t0h,unsafe_allow_html=True)
                        st.markdown(df_visu.loc[i,'Organisation'])
                    with col3:
                        t0i = 'Email'
                        s_t0i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0i}</p>"
                        st.markdown(s_t0i,unsafe_allow_html=True)
                        st.markdown(df_visu.loc[i,'Email'])

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