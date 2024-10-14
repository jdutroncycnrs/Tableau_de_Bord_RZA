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


guide = st.sidebar.button("Mode d'emploi")

if guide:
    st.title(":grey[Mode d'emploi du site]")

    tab1, tab2, tab3, tab4 =st.tabs(["Publications HAL","Données entreposées","Fiche de métadonnées", "Analyse globale du catalogue" ])

    with tab1:
        pass
    with tab2:
        pass
    with tab3:
        pass
    with tab4:
        pass

else:
    
    st.title(':grey[Science Ouverte du RZA]')

    st.subheader("Différentes pages pour visualiser des informations:")

    proposals =  f"""<span style="font-size: 26 px;">
    <ol>
    <li style="font-size:15px";>ICI , Page de Présentation</li>
    <li style="font-size:15px";></li>
    <li style="font-size:15px";></li>
    <li style="font-size:15px";></li>
    <li style="font-size:15px";></li>
    <li style="font-size:15px";></li>
    <li style="font-size:15px";></li>
    </ol></span>"""

    st.markdown(proposals, unsafe_allow_html=True)