import streamlit as st
from PIL import Image

######################################################################################################################
########### TITRE DE L'ONGLET ########################################################################################
######################################################################################################################
st.set_page_config(
    page_title="Tableau de Bord RZA",
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

st.sidebar.success("Selectionner une page ci-dessus")

######################################################################################################################
########### NUAGE DE MOTS ############################################################################################
######################################################################################################################
Nuage_mots = Image.open("pages/data/Images/nuage-de-mots.png")
left_co,center_co,last_co = st.columns(3)
with center_co:
    st.sidebar.image(Nuage_mots, width=300)

######################################################################################################################
########### LOGOS ####################################################################################################
######################################################################################################################
col1, col2 = st.columns(2)
logo1 = Image.open("pages/data/Images/logo_CNRS.png")
logo2 = Image.open("pages/data/Images/logo_RZA.png")

with col1:
    st.image(logo1, width=100)
with col2:
    st.image(logo2, width=300)


######################################################################################################################
########### TITRE ET BIENVENUE #######################################################################################
######################################################################################################################
tit = 'Bienvenue sur le Tableau de Bord'
s_tit= f"<p style='font-size:50px;color:rgb(140,140,140)'>{tit}</p>"
st.markdown(s_tit,unsafe_allow_html=True)


guide = st.sidebar.checkbox("Mode d'emploi")

if guide:
    st.title(":grey[Mode d'emploi du site]")

    tab1, tab2, tab3, tab4, tab5 =st.tabs(["Publications HAL","Données RZA","Fiche de métadonnées", "Analyse globale du catalogue", "Data Management" ])

    with tab1:
        publi_hal_guide =  f"""<span style="font-size: 35 px;">
        <span style="font-size:20px";>vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv </span>
        <span style="font-size:20px";>vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv </span>"""
        st.markdown(publi_hal_guide, unsafe_allow_html=True)
    with tab2:
        data_guide =  f"""<span style="font-size: 35 px;">
        <span style="font-size:20px";>vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv </span>
        <span style="font-size:20px";>vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv </span>"""
        st.markdown(data_guide, unsafe_allow_html=True)
    with tab3:
        fiches_guide =  f"""<span style="font-size: 35 px;">
        <span style="font-size:20px";>vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv </span>
        <span style="font-size:20px";>vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv </span>"""
        st.markdown(fiches_guide, unsafe_allow_html=True)
    with tab4:
        analyse_guide =  f"""<span style="font-size: 35 px;">
        <span style="font-size:20px";>vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv </span>
        <span style="font-size:20px";>vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv </span>"""
        st.markdown(analyse_guide, unsafe_allow_html=True)
    with tab5:
        data_mana_guide =  f"""<span style="font-size: 35 px;">
        <span style="font-size:20px";>vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv </span>
        <span style="font-size:20px";>vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv </span>"""
        st.markdown(data_mana_guide, unsafe_allow_html=True)

else:
    
    st.title(':grey[Science Ouverte du RZA]')

    st.subheader("Ce que contient ce site:")

    proposals =  f"""<span style="font-size: 35 px;">
    <ol>
    <li style="font-size:20px";> ICI : Page de présentation et mode d'emploi => Cocher la case à gauche </li>
    <li style="font-size:20px";>Page de recherche des publications sur HAL</li>
    <li style="font-size:20px";>Page de recherche des données déposées / différents entrepôts accessibles</li>
    <li style="font-size:20px";>Visualisation des fiches de métadonnées sur le catalogue InDoRES</li>
    <li style="font-size:20px";>Analyse globale du contenu du catalogue InDoRES</li>
    <li style="font-size:20px";>Une page de bilan et perspectives à traiter</li>
    </ol></span>"""

    st.markdown(proposals, unsafe_allow_html=True)