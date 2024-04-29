import streamlit as st
from PIL import Image

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Tableau de Bord RZA",
    page_icon="👋",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

col1, col2 = st.columns(2)
logo1 = Image.open("logo_CNRS.png")
logo2 = Image.open("logo_RZA.png")

with col1:
    st.image(logo1, width=100)
with col2:
    st.image(logo2, width=300)


########### TITRE DE BIENVENUE #####################################
st.title('Bienvenue sur le Tableau de Bord "Science Ouverte du RZA"')

"""
Tableau de bord du réseau des zones ateliers:
- Visualisation des indicateurs du Geonetwork
- Visualisation des indicateurs du Dataverse
"""

left_co, center_co,last_co = st.columns(3)
with center_co:
    st.image("nuage-de-mots.png", width=450)


st.sidebar.success("Selectionner une page ci-dessus")