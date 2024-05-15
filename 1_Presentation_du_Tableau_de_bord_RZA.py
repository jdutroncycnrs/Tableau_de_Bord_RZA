import streamlit as st
from PIL import Image

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Tableau de Bord RZA",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

########### LOGOS ##################################################
col1, col2 = st.columns(2)
logo1 = Image.open("logo_CNRS.png")
logo2 = Image.open("logo_RZA.png")

with col1:
    st.image(logo1, width=100)
with col2:
    st.image(logo2, width=300)


########### TITRE DE BIENVENUE #####################################
tit = 'Bienvenue sur le Tableau de Bord'
s_tit= f"<p style='font-size:50px;color:rgb(140,140,140)'>{tit}</p>"
st.markdown(s_tit,unsafe_allow_html=True)

st.title(':green[Science Ouverte du RZA]')

soustext = """Tableau de bord du réseau des zones ateliers:\n
- Visualisation des indicateurs du Geonetwork\n
- Visualisation des indicateurs du Dataverse
"""
s_soustext= f"<p style='font-size:25px;color:rgb(140,140,140)'>{soustext}</p>"
st.markdown(s_soustext,unsafe_allow_html=True)

########## NUAGE DE MOTS ###########################################
Nuage_mots = Image.open("nuage-de-mots.png")
left_co,center_co,last_co = st.columns(3)
with center_co:
    st.image(Nuage_mots, width=450)


st.sidebar.success("Selectionner une page ci-dessus")