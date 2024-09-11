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

st.title('Science Ouverte du RZA')

soustext = """Tableau de bord du réseau des zones ateliers:\n
- Visualisation générale du Geonetwork\n
Cette page propose un regard sur l'évolution générale du contenu des métadonnées récoltées (correspondantes à tous les dépôts (connus) / tout entrepôt confondu )\n
- Visualisation fiche par fiche du Geonetwork\n
Pour aller plus spécifiquement focaliser sur une fiche ou un groupe de fiches, cette page permet de visualiser les métadonnées directement\n
- Visualisation générale du Dataverse\n
Cette page propose un regard sur l'état général du contenu de l'entrepôt institutionnel Data.InDoRes\n
- Documentations\n
Pour comprendre en détails ce qui est proposé dans les différentes visualisations\n
- Référents "Données" du RZA\n
Noms et adresses email des personnes ressources pour la publication des données dans le RZA
"""
s_soustext= f"<p style='font-size:25px;color:rgb(140,140,140)'>{soustext}</p>"
st.markdown(s_soustext,unsafe_allow_html=True)

st.sidebar.success("Selectionner une page ci-dessus")

########## NUAGE DE MOTS ###########################################
Nuage_mots = Image.open("nuage-de-mots.png")
left_co,center_co,last_co = st.columns(3)
with center_co:
    st.sidebar.image(Nuage_mots, width=300)