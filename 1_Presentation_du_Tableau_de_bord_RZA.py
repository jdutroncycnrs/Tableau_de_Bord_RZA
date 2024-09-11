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

st.title(':grey[Science Ouverte du RZA]')

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


tit = 'Documentations'
s_tit= f"<p style='font-size:50px;color:rgb(140,140,140)'>{tit}</p>"
st.markdown(s_tit,unsafe_allow_html=True)

FAIR_principes = Image.open("Principes_FAIR.png")
st.image(FAIR_principes, width=1000)

tit = 'Référents "Données" du RZA'
s_tit= f"<p style='font-size:50px;color:rgb(140,140,140)'>{tit}</p>"
st.markdown(s_tit,unsafe_allow_html=True)

st.markdown('Jérôme Dutroncy, LTSER-FR Réseau des Zones Ateliers jerome.dutroncy@univ-smb.fr')

st.markdown('Cécile Pignol , Zone Atelier Alpes - cecile.pignol@univ-smb.fr')

st.markdown('A venir, Zone Atelier Arc Jurassien - ')

st.markdown('Françoise Le Moal ,  Zone Atelier Armorique - francoise.le-moal@univ-rennes1.fr')

st.markdown('Anne Clemens , Zone Atelier Bassin du Rhône - anne.clemens@graie.org')

st.markdown('A venir,  Zone Atelier Brest Iroise - ')

st.markdown('Isabelle Charpentier , Zone Atelier Environnementale Urbaine - icharpentier@unistra.fr')

st.markdown('Simon Chamaillé , Zone Atelier Hwange - simon.chamaille@cefe.cnrs.fr')

st.markdown('Annaelle Simonneau ,  Zone Atelier Loire - anaelle.simonneau@univ-orleans.fr')

st.markdown('Emmanuelle Montarges  , Zone Atelier Bassin de la Moselle - emmanuelle.montarges@univ-lorraine.fr')

st.markdown('Wilfired Heintz , Zone Atelier Pyrénées Garonne - wilfried.heintz@inrae.fr')

st.markdown('Marie Silvestre , Zone Atelier Seine - marie.silvestre@sorbonne-universite.fr')

st.markdown('David Sarramia , Zone Atelier Territoires Uranifères - david.sarramia@clermont.in2p3.fr')

st.markdown('Iris Barjhoux , Zone Atelier Environnementale Rurale - iris.barjhoux@univ-reims.fr')

st.markdown('Jean-Claude Raynal  , Zone Atelier Santé Environnement Camargue - jean-claude.raynal@cnrs.fr')