import streamlit as st
import pandas as pd
from Recuperation_uuids import scraping_GN, uuids_cleaning

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Analyse des fiches de métadonnées du GeoNetwork",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

############ PARAMETRES ############################################

URL_GN_search = "https://cat.indores.fr/geonetwork/srv/fre/catalog.search#/search?any="

with st.spinner("Connexion au GeoNetwork et récupération des identifiants existants"):
    m = scraping_GN()
    st.write(m)   
    m2 = uuids_cleaning()
    st.write(m2)