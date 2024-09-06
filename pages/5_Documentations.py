import streamlit as st
from PIL import Image

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Documentations",
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

tit = 'Documentations'
s_tit= f"<p style='font-size:50px;color:rgb(140,140,140)'>{tit}</p>"
st.markdown(s_tit,unsafe_allow_html=True)

FAIR_principes = Image.open("Principes_FAIR.png")
st.image(FAIR_principes, width=1000)

