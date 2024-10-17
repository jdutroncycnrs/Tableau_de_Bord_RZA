import pandas as pd
import streamlit as st

######################################################################################################################
########### TITRE DE L'ONGLET ########################################################################################
######################################################################################################################
st.set_page_config(
    page_title="Data Management RZA",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

######################################################################################################################
########### COULEURS DES PAGES #######################################################################################
######################################################################################################################
st.markdown("""
 <style>
    [data-testid=stSidebar] {
        background-color: rgb(6,51,87,0.2);
    }
    .st-emotion-cache-1dj0hjr {
            color: #a9dba6;
    }
    .st-emotion-cache-1q2d4ya {
            color: #3b979f;
    }
    </style>
""", unsafe_allow_html=True)


######################################################################################################################
########### PARAMETRES ###############################################################################################
######################################################################################################################

HAL = pd.read_csv("pages/data/Hal/Contenu_HAL_complet.csv", index_col=[0])

data_Indores = pd.read_csv("pages/data/Data_InDoRES/Contenu_DataInDoRES2.csv",index_col=[0])
data_RDG = pd.read_csv("pages/data/rechercheDataGouv/Contenu_RDG_complet.csv", index_col=[0])
data_dryad = pd.read_csv("pages/data/Dryad/Contenu_DRYAD_complet.csv", index_col=[0])
data_nakala = pd.read_csv("pages/data/Nakala/Contenu_NAKALA_complet.csv", index_col=[0])
data_zenodo = pd.read_csv("pages/data/Zenodo/Contenu_ZENODO_complet.csv", index_col=[0])
data_gbif = pd.read_csv("pages/data/Gbif/Contenu_GBIF_complet.csv", index_col=[0])

catalogue = pd.read_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_complet.csv", index_col=[0])

######################################################################################################################
########### FILTRE CATALOGUES ########################################################################################
######################################################################################################################

liste_ZAs_ = ["Zone atelier territoires uranifères",
              " Zone Atelier Seine",
              " Zone atelier Loire",
              " Zone atelier bassin du Rhône",
              " Zone atelier bassin de la Moselle",
              " Zone atelier Alpes",
              " Zone atelier arc jurassien",
              " Zone atelier Armorique",
              " Zone atelier Plaine et Val de Sèvre",
              " Zone atelier environnementale urbaine",
              " Zone atelier Hwange",
              " Zone atelier Pyrénées Garonne",
              " Zone atelier Brest Iroise",
              " Zone Atelier Antarctique et Terres Australes",
              " Zone Atelier Santé Environnement Camargue",
              " Zone Atelier Argonne"]


######################################################################################################################
########### SELECTION ZA #############################################################################################
######################################################################################################################

all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)