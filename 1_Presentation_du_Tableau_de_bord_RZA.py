import streamlit as st

st.set_page_config(
    page_title="Tableau de Bord RZA",
    page_icon="👋",
)

st.title('Bienvenue sur le Tableau de Bord "Science Ouverte du RZA"')

"""
Tableau de bord du réseau des zones ateliers:
- Visualisation des indicateurs du Geonetwork
- Visualisation des indicateurs du Dataverse
"""

#st.image(r"data\images\nuage-de-mots.png")
st.image("data\images\logo_CNRS.png", width=300)
st.image("data\images\logo_RZA.png",width=300)

st.sidebar.success("Select a page above.")