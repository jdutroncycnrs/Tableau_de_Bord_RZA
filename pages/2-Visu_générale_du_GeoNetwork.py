import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from preparation_tableau import prepa_date, year


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
        'Dynafor':'zapygar', 
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
    if len(selection_group)==0:
        df_selected = Selection_df
    else:
        df_selected = Selection_df[Selection_df['Mention'].isin(selection_group)]
    if len(selection_group)==0:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(Selection_df))
    else:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(df_selected))

elif checkbox1:
    
    Selection_df = tableau[tableau['Mention'].isin(liste_ZAs)]
    selection_group = st.sidebar.multiselect('choix du groupe',options=liste_ZAs)
    if len(selection_group)==0:
        df_selected = Selection_df
    else:
        df_selected = Selection_df[Selection_df['Mention'].isin(selection_group)]
    if len(selection_group)==0:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(Selection_df))
    else:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(df_selected))

else:
    Catalogues_counts = tableau['Mention'].value_counts()
    df_selected = tableau
    st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(df_selected))

##################### PREPARATION DATES ###################################################################
df_selected_year = year(df_selected)

df_selected_year_bis = df_selected_year.dropna(subset='Year')
#start_year = int(min(df_selected_year_bis['Year'].values))
#end_year = int(max(df_selected_year_bis['Year'].values))

liste_years = set(df_selected_year_bis['Year'])
start_year = int(min(liste_years))
end_year = int(max(liste_years))

rule = '6ME'
df_date = prepa_date(df_selected_year, rule=rule)
df_date_year = year(df_date)

##################### Choix d'une période #################################################################

selection_dates_input = st.sidebar.slider('DATE MINI CHOISIE',min_value=start_year,max_value=end_year)

###########################################################################################################
with st.container(border=True):

    if 'Repartition_fiches' not in st.session_state:
        st.session_state.Repartition_fiches = False
    if 'Evolution_temporelle' not in st.session_state:
        st.session_state.Evolution_temporelle = False
    if 'Repartition_spatiale' not in st.session_state:
        st.session_state.Repartition_spatiale = False
    if 'Autres_champs' not in st.session_state:
        st.session_state.Repartition_spatiale = False
    if 'Description' not in st.session_state:
        st.session_state.Repartition_spatiale = False
    if 'Analyse_FAIR' not in st.session_state:
        st.session_state.Repartition_spatiale = False

    # Function to handle checkbox1 change
    def handle_button1_change():
        if st.session_state.Repartition_fiches:
            st.session_state.Evolution_temporelle = False
            st.session_state.Repartition_spatiale = False
            st.session_state.Autres_champs = False
            st.session_state.Description = False
            st.session_state.Analyse_FAIR = False

    def handle_button2_change():
        if st.session_state.Evolution_temporelle:
            st.session_state.Repartition_spatiale = False
            st.session_state.Autres_champs = False
            st.session_state.Description = False
            st.session_state.Analyse_FAIR = False
            st.session_state.Repartition_fiches = False

    # Function to handle checkbox2 change
    def handle_button3_change():
        if st.session_state.Repartition_spatiale:
            st.session_state.Evolution_temporelle = False
            st.session_state.Autres_champs = False
            st.session_state.Description = False
            st.session_state.Analyse_FAIR = False
            st.session_state.Repartition_fiches = False

    def handle_button4_change():
        if st.session_state.Autres_champs:
            st.session_state.Evolution_temporelle = False
            st.session_state.Repartition_spatiale = False
            st.session_state.Description = False
            st.session_state.Analyse_FAIR = False
            st.session_state.Repartition_fiches = False

    def handle_button5_change():
        if st.session_state.Description:
            st.session_state.Evolution_temporelle = False
            st.session_state.Repartition_spatiale = False
            st.session_state.Autres_champs = False
            st.session_state.Analyse_FAIR = False
            st.session_state.Repartition_fiches = False

    def handle_button6_change():
        if st.session_state.Analyse_FAIR:
            st.session_state.Evolution_temporelle = False
            st.session_state.Repartition_spatiale = False
            st.session_state.Autres_champs = False
            st.session_state.Description = False
            st.session_state.Repartition_fiches = False

    col1,col2,col3,col4,col5,col6 = st.columns(6)
    with col1:
        Repartition_fiches = st.checkbox(label='Répartition des fiches', key='Repartition_fiches',on_change=handle_button1_change)
    with col2:
        Evolution_temporelle = st.checkbox(label='Evolution temporelle', key='Evolution_temporelle',on_change=handle_button2_change)
    with col3:
        Repartition_spatiale = st.checkbox(label='Répartition spatiale', key='Repartition_spatiale',on_change=handle_button3_change)
    with col4:
        Autres_champs = st.checkbox(label='Autres champs', key='Autres_champs',on_change=handle_button4_change)
    with col5:
        Description = st.checkbox(label='Descriptions', key='Description',on_change=handle_button5_change)
    with col6:
        Analyse_FAIR = st.checkbox(label='Analyse FAIR', key='Analyse_FAIR',on_change=handle_button6_change)


if Repartition_fiches:
    Counts = df_selected_year['Mention'].value_counts()
    fig_counts = px.pie(values=Counts.values, 
                    names=Counts.index)
    fig_counts.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                                marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig_counts.update_layout(
                    title='Répartition des fiches dans les catalogues',
                    width=500,
                    height=800)
    st.plotly_chart(fig_counts,use_container_width=True)

elif Evolution_temporelle:
    
    fig_tempo = go.Figure()
    fig_tempo.add_trace(go.Bar(
            x=df_date_year['Date'][df_date_year.Year >= selection_dates_input],
            y=df_date_year['Compte_resampled'][df_date_year.Year >= selection_dates_input],
            name='Dates',
            marker=dict(color='#90B7CF',line=dict(color='#90B7CF',width=3))))
    fig_tempo.update_layout(title='Dates des fiches',
                xaxis_title='Dates',
                yaxis_title='Compte semestriel',
                width=500,
                height=500)
    st.plotly_chart(fig_tempo, use_container_width=True)


elif Repartition_spatiale:
    st.write('en cours de fabrication')

elif Autres_champs:
    with st.container(border=True):
        if 'Langues' not in st.session_state:
            st.session_state.Langues = False
        if 'Standards' not in st.session_state:
            st.session_state.Standards = False
        if 'Formats' not in st.session_state:
            st.session_state.Formats = False
        if 'Orgas' not in st.session_state:
            st.session_state.Orgas = False
        if 'Contacts' not in st.session_state:
            st.session_state.Contacts = False
        if 'Droits' not in st.session_state:
            st.session_state.Droits = False

        # Function to handle checkbox1 change
        def handle_button1_change():
            if st.session_state.Langues:
                st.session_state.Standards = False
                st.session_state.Formats = False
                st.session_state.Orgas = False
                st.session_state.Contacts = False
                st.session_state.Droits = False

        def handle_button2_change():
            if st.session_state.Standards:
                st.session_state.Langues = False
                st.session_state.Formats = False
                st.session_state.Orgas = False
                st.session_state.Contacts = False
                st.session_state.Droits = False

        # Function to handle checkbox2 change
        def handle_button3_change():
            if st.session_state.Formats:
                st.session_state.Standards = False
                st.session_state.Langues = False
                st.session_state.Orgas = False
                st.session_state.Contacts = False
                st.session_state.Droits = False

        def handle_button4_change():
            if st.session_state.Orgas:
                st.session_state.Standards = False
                st.session_state.Formats = False
                st.session_state.Langues = False
                st.session_state.Contacts = False
                st.session_state.Droits = False

        def handle_button5_change():
            if st.session_state.Contacts:
                st.session_state.Standards = False
                st.session_state.Formats = False
                st.session_state.Orgas = False
                st.session_state.Langues = False
                st.session_state.Droits = False

        def handle_button6_change():
            if st.session_state.Droits:
                st.session_state.Standards = False
                st.session_state.Formats = False
                st.session_state.Orgas = False
                st.session_state.Contacts = False
                st.session_state.Langues = False

        col1,col2,col3,col4,col5,col6 = st.columns(6)
        with col1:
            Langues = st.checkbox(label='Langues utilisées', key='Langues',on_change=handle_button1_change)
        with col2:
            Standards = st.checkbox(label='Standards utilisés', key='Standards',on_change=handle_button2_change)
        with col3:
            Formats = st.checkbox(label='Formats utilisés', key='Formats',on_change=handle_button3_change)
        with col4:
            Orgas = st.checkbox(label='Organisations identifiées', key='Orgas',on_change=handle_button4_change)
        with col5:
            Contacts = st.checkbox(label='Contacts identifiés', key='Contacts',on_change=handle_button5_change)
        with col6:
            Droits = st.checkbox(label='Droits / Licences', key='Droits',on_change=handle_button6_change)

    if Langues:
        st.write('en cours de fabrication')
    elif Standards:
        st.write('en cours de fabrication')
    elif Formats:
        st.write('en cours de fabrication')
    elif Orgas:
        st.write('en cours de fabrication')
    elif Contacts:
        st.write('en cours de fabrication')
    elif Droits:
        st.write('en cours de fabrication')

elif Description:
    st.write('en cours de fabrication')

elif Analyse_FAIR:
    st.write('en cours de fabrication')

st.dataframe(df_selected)
