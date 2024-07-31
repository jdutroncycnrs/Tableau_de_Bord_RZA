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

group_ = pd.read_csv("pages/data/infos_MD/infos_groupes_mentions.csv", index_col=[0])

tableau = pd.read_csv("pages/data/infos_MD/Tableau_MD.csv", index_col=[0])

dico = {'ZABrI - Brest Iroise':'zabri', 
        'Pas de fichier':'Aucun groupe et aucune mention', 
        'OHM Pyrénées - haut Vicdessos':'OHM Pyrénées - haut Vicdessos', 
        'OHMi Téssékéré':'OHMi Téssékéré', 
        'InDoRES':'Catalogue InDoRes', 
        'zapygar':'zapygar', 
        'OHM Littoral Caraïbe':'OHM Littoral Caraïbe', 
        'ZA':'Réseau ZA', 
        'zaar':'zaar', 
        'OHMi Nunavik':'OHMi Nunavik', 
        'zas':'zas',
        'Dynafor':'Dynafor', 
        'Groupe exemple':'Groupe exemple', 
        'OHM Pays de Bitche':'OHM Pays de Bitche', 
        'OHM Vallée du Rhône':'OHM Vallée du Rhône', 
        'OHMi Estarreja':'OHMi Estarreja', 
        'zaaj':'zaaj', 
        'Aucun groupe et aucune mention':'Aucun groupe et aucune mention', 
        'ZAA':'zaa', 
        'ZAAr':'zaar', 
        'DRIIHM':'Réseau OHM', 
        'zaeu':'zaeu', 
        'OHM Oyapock':'OHM Oyapock', 
        'OHM Bassin Minier de Provence':'OHM Bassin Minier de Provence', 
        'OHMi Pima County':'OHMi Pima County', 
        'zabri':'zabri', 
        'zam':'zam', 
        'ZABRI':'zabri', 
        'zal':'zal', 
        'OHM Littoral méditerranéen':'OHM Littoral méditerranéen', 
        'zaa':'zaa', 
        'zabr':'zabr'}

group_['Groupe_et_Mention'] = group_['Groupe_et_Mention'].map(dico)
tableau['Mention'] = tableau['Mention'].map(dico)

colors = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0']

###########  FILTRE DES CATALOGUES ####################################
liste_groupes = set(group_['Groupe_et_Mention'].values)

liste_ZAs = ['zaa', 
             'zaaj', 
             'zal',
             'zaar',
             'zabr',
             'zabri', 
             'zaeu',
             'zapygar', 
             'zam', 
             'zas',
             'zah',
             'zatu',
             'zata',
             'zarg',
             'zacam',
             'zapvs',
             'RZA', #RZA
             ]
liste_OHMs = ['OHM Littoral méditerranéen',
              'OHM Oyapock','OHM Pyrénées - haut Vicdessos',
              'OHM Bassin Minier de Provence',
              'OHMi Pima County',
              'OHMi Nunavik',
              'OHMi Téssékéré',
              'OHMi Estarreja',
              'OHM Vallée du Rhône',
              'OHM Pays de Bitche',
              'OHM Littoral Caraïbe',
              'DRIIHM']
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
    Selection_df = tableau[tableau['Mention'].isin(liste_OHMs)]
    selection_group = st.sidebar.multiselect('choix du groupe',options=liste_OHMs)
    df_groupe = Selection_df[Selection_df['Mention'].isin(selection_group)]
    if len(selection_group)==0:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(Selection_df))
    else:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(df_groupe))

elif checkbox1:
    
    Selection_df = tableau[tableau['Mention'].isin(liste_ZAs)]
    selection_group = st.sidebar.multiselect('choix du groupe',options=liste_ZAs)
    df_groupe = Selection_df[Selection_df['Mention'].isin(selection_group)]
    if len(selection_group)==0:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(Selection_df))
    else:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(df_groupe))

else:
    Catalogues_counts = tableau['Mention'].value_counts()
    Selection_df = tableau
    st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(Selection_df))


Repartition_fiches = st.button(label='Répartition des fiches')

if Repartition_fiches:
    Counts = Selection_df['Mention'].value_counts()
    fig = px.pie(values=Counts.values, 
                names=Counts.index)
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                            marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(
                title='Répartition des fiches dans les catalogues',
                width=500,
                height=800)
    st.plotly_chart(fig,use_container_width=True)



st.dataframe(Selection_df)
st.dataframe(df_groupe)