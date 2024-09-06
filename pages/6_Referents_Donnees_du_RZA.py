import streamlit as st

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Referents Donnees du RZA",
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
        background-color: rgb(6,51,87);
    }
    .st-emotion-cache-1dj0hjr {
            color: #cbd117;
    }
    .st-emotion-cache-1rtdyuf {
            color: #cbd117;
    }
    .st-emotion-cache-6tkfeg {
            color: #cbd117;
    }
    .st-emotion-cache-1q2d4ya {
            color: #cbd117;
    }
    </style>
""", unsafe_allow_html=True)


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