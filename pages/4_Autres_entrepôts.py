import streamlit as st
from PIL import Image
import pandas as pd
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi
import glob
import datetime
import plotly.express as px
import requests


from Recuperation_dataverses import Recup_dataverses, Recup_contenu_dataverse, Recup_dataverses_rdg, recuperation_zenodo, recuperation_nakala, recuperation_dryad, recuperation_gbif

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Autres entrepôts",
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
BASE_URL="https://entrepot.recherche.data.gouv.fr/"
API_TOKEN="b02fd46a-2fb0-4ac3-8717-ae70ec35185a"

######################## Nakala ############################################
url_nakala = "https://api.nakala.fr/search"
headers_nakala = {
  'X-API-KEY': 'c3cac1e9-cecc-a05c-bf8e-2459669a1f31',
  'accept': 'application/json'
}

######################## Zenodo ############################################
url_zenodo = 'https://zenodo.org/api/records/'
zenodo_token = "OMMGEVUcApEKSt4JEkSK7OzpqZQPMvGKAlB2yP2MXG6APstRn2hWpiHfpjaA"
headers_zenodo = {"Content-Type": "application/json"}

########################## DRYAD #########################################
url_dryad = "https://datadryad.org/api/v2/search?"


########################## GBIF #########################################
url_gbif = "https://api.gbif.org/v1/dataset?q=alpes"
headers_gbif = {'accept': 'application/json'}


########### CHOIX ZA ######################################
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


all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)


###################### CREATION CONNEXION ##############################
Choix_entrepot = st.sidebar.subheader('Entrepôts')
with st.sidebar:
    if 'rdg' not in st.session_state:
        st.session_state.rdg = False
    if 'nakala' not in st.session_state:
        st.session_state.nakala = False
    if 'zenodo' not in st.session_state:
        st.session_state.zenodo = False
    if 'dryad' not in st.session_state:
        st.session_state.dryad = False
    if 'gbif' not in st.session_state:
        st.session_state.gbif = False

    # Function to handle checkbox1 change
    def handle_checkbox1_change():
        if st.session_state.rdg:
            st.session_state.nakala = False
            st.session_state.zenodo = False
            st.session_state.nakala = False
            st.session_state.zenodo = False
            

    # Function to handle checkbox2 change
    def handle_checkbox2_change():
        if st.session_state.nakala:
            st.session_state.rdg = False
            st.session_state.zenodo = False
            st.session_state.dryad = False
            st.session_state.gbif = False

    def handle_checkbox3_change():
        if st.session_state.zenodo:
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.dryad = False
            st.session_state.gbif = False
    
    def handle_checkbox4_change():
        if st.session_state.dryad:
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.gbif = False
            st.session_state.zenodo = False
    
    def handle_checkbox5_change():
        if st.session_state.gbif:
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.dryad = False
            st.session_state.zenodo = False

    choix_groupe_OHM = False
    rdg = st.checkbox("RGD", key='rdg', on_change=handle_checkbox1_change)
    nakala = st.checkbox("NAKALA", key='nakala', on_change=handle_checkbox2_change)
    zenodo = st.checkbox("ZENODO", key='zenodo', on_change=handle_checkbox3_change)
    dryad = st.checkbox("DRYAD", key='dryad', on_change=handle_checkbox4_change)
    gbif = st.checkbox("GBIF", key='gbif', on_change=handle_checkbox5_change)


if rdg:
    st.title(":grey[Analyse des dépôts dans Recherche Data Gouv]")

    adresse_RDG = 'https://entrepot.recherche.data.gouv.fr/dataverse/root?q='
    s_adresse_RDG = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_RDG}</p>"
    st.markdown(s_adresse_RDG ,unsafe_allow_html=True)

    with st.spinner("Connexion au Dataverse Recherche Data Gouv en cours"):
        api = NativeApi(BASE_URL, API_TOKEN)
        resp = api.get_info_version()
        response = resp.json()

    if response['status']=='OK':
        st.write(f"La connexion est établie avec Recherche Data Gouv")
    else: 
        st.write(f"La connexion a échoué, vous n'êtes pas connecté à Recherche Data Gouv")


    d = datetime.date.today()

    fichier = f'tableau_dataverses_rdg-{d}.csv'

    fi = glob.glob(f"pages/data/rechercheDataGouv/tableau_dataverses*.csv")

    Choix_rdg = st.sidebar.subheader('RDG sélectionné')

    visu_sunburst= st.sidebar.checkbox("Voir l'ensemble des entrepôts existants")

    if len(fi)!=0:
        fich = fi[-1]
        dataverses = pd.read_csv(fich)
        if visu_sunburst:
            fig = px.sunburst(dataverses, path=['niv0','niv1','niv2'], values='val')
            fig.update_layout(
                title=f'Visuel des différents Dataverses dans RDG via {fich}',
                width=1000,
                height=1000)
            st.plotly_chart(fig,use_container_width=True)
    else:
        st.write('Il est nécessaire de mettre à jour vos entrepôts')


    ##########POUR L'ADMINISTRATEUR ########################################
    admin_pass = 'admin'
    admin_action = st.sidebar.text_input(label="Pour l'administrateur")

    if admin_action == admin_pass:
        b1 = st.sidebar.button(label=" Mise à jour des entrepôts Dataverses dans RDG ")

        if b1==True:
            with st.spinner("Récupération des entrepôts existants"):
                Recup_dataverses_rdg(api,fichier)
    ############################################################################

if nakala:
    s = " ZA alpes"
    params_nakala = {'q': f'{s}'}
    r = recuperation_nakala(url_nakala,params_nakala, headers_nakala, s)
    st.write(r)

if zenodo:
    st.title(":grey[Analyse des dépôts dans Zenodo]")

    adresse_zenodo = url_zenodo
    s_adresse_zenodo = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_zenodo}</p>"
    st.markdown(s_adresse_zenodo ,unsafe_allow_html=True)

    liste_columns = ['ZA','Ids','Titre']
    df_global = pd.DataFrame(columns=liste_columns)
    for i, s in enumerate(Selection_ZA):
        params_zenodo = {'q': f'{s}',
                 'access_token': zenodo_token}
        df = recuperation_zenodo(url_zenodo,params_zenodo, headers_zenodo, s)
        dfi = pd.concat([df_global,df], axis=0)
        dfi.reset_index(inplace=True)
        dfi.drop(columns='index', inplace=True)
        df_global = dfi
    df_global.sort_values(by='Ids', inplace=True, ascending=False)
    df_global.reset_index(inplace=True)
    df_global.drop(columns='index', inplace=True)

    if len(df_global)==0:
        pass
    else:
        st.metric(label="Nombre de publications trouvées", value=len(df_global))
        st.table(df_global)

if dryad:
    params_dryad = {'q':'zone atelier alpes'}
    r = recuperation_dryad(url_dryad,params_dryad)
    st.write(r)


if gbif:
    params_gbif = {'q':'alpes'}
    r = recuperation_gbif(url_gbif,params_gbif, headers_gbif)
    st.write(r)