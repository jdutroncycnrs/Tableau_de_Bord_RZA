import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Analyse globale des enregistrements dans le GeoNetwork",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

############ PARAMETRES ############################################

group_ = pd.read_csv("pages/data/infos_MD/infos_groupes.csv", index_col=[0])

colors = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0']

###########  FILTRE DES CATALOGUES ####################################
#liste_groupes = set(group_['Groupe'].values)

liste_ZAs = ['zaa', 'zal','zaar','zabr','zaeu','ZA','zapygar', 'zaaj', 'zabri', 'zam', 'zas']
liste_OHMs = ['OHM Littoral méditerranéen','OHM Oyapock','OHM Pyrénées - haut Vicdessos','DRIIHM','OHM Bassin Minier de Provence','OHMi Pima County','OHMi Nunavik','OHMi Téssékéré','OHMi Estarreja','OHM Vallée du Rhône','OHM Pays de Bitche']
autres = ['Groupe exemple','Dynafor','InDoRES','Aucun groupe']

########### Choix OHM/RZA #############################################################
## Le choix est exclusif ##############################################################
if 'checkbox1' not in st.session_state:
    st.session_state.checkbox1 = False
if 'checkbox2' not in st.session_state:
    st.session_state.checkbox2 = False

# Function to handle checkbox1 change
def handle_checkbox1_change():
    if st.session_state.checkbox1:
        st.session_state.checkbox2 = False

# Function to handle checkbox2 change
def handle_checkbox2_change():
    if st.session_state.checkbox2:
        st.session_state.checkbox1 = False

col1,col2 =st.sidebar.columns(2)
choix_groupe_OHM = False
with col1:
    checkbox1 = st.checkbox("RZA", key='checkbox1', on_change=handle_checkbox1_change)
with col2:
    checkbox2 = st.checkbox("OHM", key='checkbox2', on_change=handle_checkbox2_change)


if checkbox2:
    OHMs_df = group_[group_['Groupe'].isin(liste_OHMs)]
    OHMs_counts = OHMs_df['Groupe'].value_counts()
    fig = px.pie(values=OHMs_counts.values, 
             names=OHMs_counts.index)
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                        marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(
            title='Répartition des fiches dans les catalogues OHM',
            width=700,
            height=700)
    st.plotly_chart(fig,use_container_width=True)
elif checkbox1:
    ZAs_df = group_[group_['Groupe'].isin(liste_ZAs)]
    ZAs_counts = ZAs_df['Groupe'].value_counts()
    fig = px.pie(values=ZAs_counts.values, 
             names=ZAs_counts.index)
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                        marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(
            title='Répartition des fiches dans les catalogues ZA',
            width=700,
            height=700)
    st.plotly_chart(fig,use_container_width=True)
else:
    Catalogues_counts = group_['Groupe'].value_counts()

    fig = px.pie(values=Catalogues_counts.values, 
                names=Catalogues_counts.index)
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                        marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(
            title='Répartition des fiches dans les catalogues',
            width=700,
            height=700)
    st.plotly_chart(fig,use_container_width=True)