import streamlit as st
from PIL import Image

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Tableau de Bord RZA",
    page_icon="👋",
)

########### TITRE DE BIENVENUE #####################################
st.title('Bienvenue sur le Tableau de Bord "Science Ouverte du RZA"')

"""
Tableau de bord du réseau des zones ateliers:
- Visualisation des indicateurs du Geonetwork
- Visualisation des indicateurs du Dataverse
"""

#st.image(r"data\images\nuage-de-mots.png")
st.image(Image.open(".\data\images\logo_CNRS.png"), width=300, caption='logo du CNRS')
st.image(Image.open(".\data\images\logo_RZA.png"),width=300, caption='logo du RZA')

st.sidebar.success("Selectionner une page ci-dessus")