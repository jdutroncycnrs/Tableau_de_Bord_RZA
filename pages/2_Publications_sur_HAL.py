import streamlit as st
from PIL import Image
from Publications import afficher_publications_hal
import pandas as pd

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Publications du RZA sur HAL",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

########### COULEURS SIDEBAR ######################################
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

########### CHOIX ZA ######################################
liste_ZAs_ = ["Zone atelier territoires uranifères",
              " Zone Atelier Seine",
              " Zone atelier Loire",
              " Zone atelier bassin du Rhône",
              " Zone atelier bassin de la Moselle",
              " Zone atelier Alpes",
              " Zone atelier arc jurassien",
              " Zone atelier Armorique",
              " Zone atelier Plaine et Val de Sèvre",
              " Zone atelier environnementale urbaine",
              " Zone atelier Hwange",
              " Zone atelier Pyrénées Garonne",
              " Zone atelier Brest Iroise",
              " Zone Atelier Antarctique et Terres Australes",
              " Zone Atelier Santé Environnement Camargue",
              " Zone Atelier Argonne"]


all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)


st.title(":grey[Analyse des publications sur HAL]")


liste_columns = ['ZA','Ids','Titre et auteurs','Uri','Type','Type de document']
df_global = pd.DataFrame(columns=liste_columns)
for i, s in enumerate(Selection_ZA):
        url_type = f'http://api.archives-ouvertes.fr/search/?q=text:{s.lower().strip()}&wt=json&sort=docid asc&fl=docid,label_s,uri_s,submitType_s,docType_s'
        df = afficher_publications_hal(url_type, s)
        dfi = pd.concat([df_global,df], axis=0)
        dfi.reset_index(inplace=True)
        dfi.drop(columns='index', inplace=True)
        df_global = dfi
df_global.sort_values(by='Ids', inplace=True, ascending=False)
df_global.reset_index(inplace=True)
df_global.drop(columns='index', inplace=True)

if len(df_global)==0:
     pass
else:
        st.metric(label="Nombre de publications trouvées", value=len(df_global))
        st.table(df_global)