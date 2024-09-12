import streamlit as st
from PIL import Image
import pandas as pd
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi
import glob
import datetime
import plotly.express as px


from Recuperation_dataverses import Recup_dataverses, Recup_contenu_dataverse, Recup_dataverses_rdg

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
##########################################################################
st.title(":grey[Analyse des dépôts dans Recherche Data Gouv]")

adresse_RDG = 'https://entrepot.recherche.data.gouv.fr/dataverse/root?q='
s_adresse_RDG = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_RDG}</p>"
st.markdown(s_adresse_RDG ,unsafe_allow_html=True)


###################### CREATION CONNEXION ##############################
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

##########POUR L'ADMINISTRATEUR ########################################
admin_pass = 'admin'
admin_action = st.sidebar.text_input(label="Pour l'administrateur")

if admin_action == admin_pass:
    b1 = st.sidebar.button(label=" Mise à jour des entrepôts Dataverses dans RDG ")

    if b1==True:
        with st.spinner("Récupération des entrepôts existants"):
            Recup_dataverses_rdg(api,fichier)
############################################################################

fi = glob.glob(f"pages/data/rechercheDataGouv/tableau_dataverses*.csv")

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