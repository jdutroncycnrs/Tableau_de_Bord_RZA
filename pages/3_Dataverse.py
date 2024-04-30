import streamlit as st

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

st.title("Analyse des entrepôts")
liste_ZAs= ['ZA1','ZA2','ZA3']
Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs)

with st.container(border=True):
    row1 = st.columns(2)

    with row1[0]:
        st.write('à remplir')
    with row1[1]:
        st.write('à remplir')

with st.container(border=True):
    row2 = st.columns(2)

    with row2[0]:
        st.write('à remplir')
    with row2[1]:
        st.write('à remplir')