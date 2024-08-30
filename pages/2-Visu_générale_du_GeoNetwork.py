import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import re
from plotly.subplots import make_subplots
from preparation_tableau import prepa_date, year, coordonnees, traitement_thesaurus
pd.options.mode.chained_assignment = None


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
zoom = 4

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
tableau['Groupe_et_Mention'] = tableau['Groupe_et_Mention'].map(dico)

colors = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0','#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0']

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
    Selection_df = tableau[tableau['Groupe_et_Mention'].isin(liste_OHMs)]
    Selection_group = st.sidebar.multiselect('choix du groupe',options=liste_OHMs)
    if len(Selection_group)==0:
        df_selected = Selection_df
    else:
        df_selected = Selection_df[Selection_df['Groupe_et_Mention'].isin(Selection_group)]
    if len(Selection_group)==0:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(Selection_df))
    else:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(df_selected))

elif checkbox1:
    
    Selection_df = tableau[tableau['Groupe_et_Mention'].isin(liste_ZAs)]
    Selection_group = st.sidebar.multiselect('choix du groupe',options=liste_ZAs)
    if len(Selection_group)==0:
        df_selected = Selection_df
    else:
        df_selected = Selection_df[Selection_df['Groupe_et_Mention'].isin(Selection_group)]
    if len(Selection_group)==0:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(Selection_df))
    else:
        st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(df_selected))

else:
    Catalogues_counts = tableau['Groupe_et_Mention'].value_counts()
    df_selected = tableau
    st.sidebar.metric('NOMBRE FICHES COMPTABILISEES:',len(df_selected))

##################### PREPARATION DATES ###################################################################
df_selected_year = year(df_selected)
try:
    df_selected_year_bis = df_selected_year.dropna(subset='Year')
    liste_years = set(df_selected_year_bis['Year'])
    start_year = int(min(liste_years))-1
    end_year = int(max(liste_years)) +1
except:
    start_year = 2024
    end_year = 2024 +1

rule = '6ME'
df_date = prepa_date(df_selected_year, rule=rule)
df_date_year = year(df_date)

##################### PREPARATION COORDONNEES SPATIALES ####################################################

df_selected_year_coord = coordonnees(df_selected_year)

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
    selection_dates_input = st.sidebar.slider('DATE MINI CHOISIE',min_value=start_year,max_value=end_year, disabled=True)
    Counts = df_selected_year['Groupe_et_Mention'].value_counts()
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
    selection_dates_input = st.sidebar.slider('DATE MINI CHOISIE',min_value=start_year,max_value=end_year, disabled=False)
    fig_tempo = go.Figure()
    try:
        fig_tempo.add_trace(go.Bar(
                x=df_date_year['Date'][df_date_year.Year >= selection_dates_input],
                y=df_date_year['Compte_resampled'][df_date_year.Year >= selection_dates_input],
                name='Dates',
                marker=dict(color='#90B7CF',line=dict(color='#90B7CF',width=3))))
    except:
        pass
    fig_tempo.update_layout(title='Dates des fiches',
                xaxis_title='Dates',
                yaxis_title='Compte semestriel',
                width=500,
                height=500)
    st.plotly_chart(fig_tempo, use_container_width=True)


elif Repartition_spatiale:
    selection_dates_input = st.sidebar.slider('DATE MINI CHOISIE',min_value=start_year,max_value=end_year, disabled=False)
    df_selected_year_coord_dropna1 = df_selected_year_coord.dropna(subset='lat')
    df_selected_year_coord_dropna2 = df_selected_year_coord_dropna1.dropna(subset='long')
    df_selected_map = df_selected_year_coord_dropna2[df_selected_year_coord_dropna2['lat']>40]
    try:
        st.map(df_selected_map[df_selected_map.Year >= selection_dates_input],latitude='lat',longitude='long',zoom=zoom,color='#FEBB5F')
    except:
        st.markdown("Désolé il n'y a pas de coordonnées à visualiser")

elif Autres_champs:
    selection_dates_input = st.sidebar.slider('DATE MINI CHOISIE',min_value=start_year,max_value=end_year, disabled=False)
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
        df_selected_year_Langue = df_selected_year['Langue'][df_selected_year.Year >= selection_dates_input]
        cnt_langue = df_selected_year_Langue.value_counts()
        fig_langue = go.Figure()
        fig_langue.add_trace(go.Pie(labels=cnt_langue.index.values, values=cnt_langue.values))
        fig_langue.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig_langue.update_layout(
                title='Langues utilisées',
                xaxis_title='Compte',
                yaxis_title='langues',
                width=1000,
                height=1000)
        st.plotly_chart(fig_langue)

    elif Standards:
        df_selected_year_Standard = df_selected_year['Standard'][df_selected_year.Year >= selection_dates_input]
        cnt_standard = df_selected_year_Standard.value_counts()
        fig_standard = go.Figure()
        fig_standard.add_trace(go.Pie(labels=cnt_standard.index.values, values=cnt_standard.values))
        fig_standard.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig_standard.update_layout(
                title='Standards utilisés',
                xaxis_title='Compte',
                yaxis_title='Standards',
                width=1000,
                height=1000)
        st.plotly_chart(fig_standard)

    elif Formats:
        df_selected_year_format = df_selected_year['Format'][df_selected_year.Year >= selection_dates_input]
        cnt_format = df_selected_year_format.value_counts()[0:15]
        somme_formats_vis = cnt_format.values.sum()

        fig_format = go.Figure()
        for i in range(10):
            cnt_orga_ = df_selected_year_format.value_counts()[i:i+1]
            fig_format.add_trace(go.Bar(
                        y=cnt_orga_.index.values,
                        x=cnt_orga_.values,
                        orientation='h',
                        showlegend=False,
                        marker=dict(color=colors[i])
                        ))
        fig_format.update_layout(
                title='Formats publiantes',
                xaxis_title='Compte',
                width=500,
                height=500)
        st.plotly_chart(fig_format)

    elif Orgas:
        df_selected_year_orga = df_selected_year['Orga_contact'][df_selected_year.Year >= selection_dates_input]
        cnt_orga = df_selected_year_orga.value_counts()[0:10]
        somme_orga_vis = cnt_orga.values.sum()
            
        fig_orga = go.Figure()
        for i in range(10):
            cnt_orga_ = df_selected_year_orga.value_counts()[i:i+1]
            fig_orga.add_trace(go.Bar(
                        y=cnt_orga_.index.values,
                        x=cnt_orga_.values,
                        orientation='h',
                        showlegend=False,
                        marker=dict(color=colors[i])
                        ))
        fig_orga.update_layout(
                title='Organisations publiantes',
                xaxis_title='Compte',
                width=500,
                height=500)
        st.plotly_chart(fig_orga)


    elif Contacts:
        
        
        st.write('en cours de fabrication')

    elif Droits:
        df_selected_year_droits = df_selected_year['Contrainte_usage'][df_selected_year.Year >= selection_dates_input]
        cnt_droits = df_selected_year_droits.value_counts()[0:15]
        somme_droits_vis = cnt_droits.values.sum()
        
        fig_droits = go.Figure()
        fig_droits.add_trace(go.Pie(labels=cnt_droits.index.values, values=cnt_droits.values))
        fig_droits.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig_droits.update_layout(
                title='Droits à usage',
                xaxis_title='Compte',
                yaxis_title='Droits',
                width=1000,
                height=1000)
        st.plotly_chart(fig_droits)


elif Description:
    selection_dates_input = st.sidebar.slider('DATE MINI CHOISIE',min_value=start_year,max_value=end_year, disabled=False)
    liste_desc = ['Themes','Thesaurus','Mots_clés']
    df_description = df_selected_year[liste_desc][df_selected_year.Year >= selection_dates_input]
    df_description_ = df_description.assign(Thesaurus_usage=0)
    df_thesaurus = df_description_[['Thesaurus','Thesaurus_usage']]

    df_thesaurus_ , df_thesaurus_oui , df_thesaurus_non = traitement_thesaurus(df_thesaurus)

    with st.container(border=True):
        col1,col2 = st.columns([0.4,0.6])
        with col1:
            cnt_usage_thesaurus = df_thesaurus_['Thesaurus_usage'].value_counts()
            somme_usage_thesaurus_vis = cnt_usage_thesaurus.values.sum()
                
            fig_usage_thesaurus = go.Figure()
            fig_usage_thesaurus.add_trace(go.Pie(labels=cnt_usage_thesaurus.index.values, values=cnt_usage_thesaurus.values))
            fig_usage_thesaurus.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                            marker=dict(colors=colors, line=dict(color='#000000', width=2)))
            fig_usage_thesaurus.update_layout(
                        title='Usage des thésaurus',
                        xaxis_title='Compte',
                        yaxis_title='Usage',
                        width=500,
                        height=500)
            st.plotly_chart(fig_usage_thesaurus)

        with col2:
            cnt_thesaurus = df_thesaurus_oui['Thesaurus_listed'].value_counts()[0:25]
            df = pd.DataFrame(cnt_thesaurus.index)
            df['count']=cnt_thesaurus.values

            liste_thesaurus = ['GEMET - INSPIRE themes', 'GEMET - Concepts', 'Régions administratives de France', 
                            'Continents countries sea regions of the world','theme.EnvironnementFR.rdf','theme.thesaurus_costel.rdf', 'Vocabulaire MétaZABR','ENVTHES','réseau des zones ateliers',
                            'Nouvelles Régions de France','external.place.inspire-theme','external.place.localisation','external.place.ore','external.place.thematiques',
                            'external.place.departements','AGROVOC','Biodiversity Thesaurus','GéoBretagne v 2.0']
            
            liste_df_count = ['A_count', 'B_count', 'C_count','D_count','E_count','F_count','G_count','H_count','I_count','J_count','K_count','L_count','M_count','N_count','O_count','P_count','Q_count','R_count']
            # Expand combinations into separate columns
            for elem in liste_thesaurus:
                df[elem] = df['Thesaurus_listed'].apply(lambda x: elem in x)

            # Multiply each by the counts
            for i in range(len(liste_thesaurus)):
                df[liste_df_count[i]] = df[liste_thesaurus[i]] * df['count']
            
            # Sum counts by element
            summed_df = df[liste_df_count].sum()

            # Create a bar plot
            fig = go.Figure()
            for i in range(len(liste_thesaurus)):
                fig.add_trace(go.Bar(
                    x=[liste_thesaurus[i]],
                    y=[summed_df[liste_df_count[i]]],
                    name=liste_thesaurus[i],
                    marker_color=colors[i]
                ))

            # Update layout for stacked bar chart
            fig.update_layout(
                barmode='stack',
                title='Thésaurus utilisés',
                xaxis=dict(title='Thesaurus'),
                yaxis=dict(title='Counts'),
                height=600,
                showlegend=False
            )

            st.plotly_chart(fig)
    
    with st.container(border=True):
        col1,col2 = st.columns(2)
        with col2:
            #df_selected_year_usage_thesaurus_non = Desc[Desc['Thesaurus_usage']=='NON']
            st.write('à venir')


elif Analyse_FAIR:
    selection_dates_input = st.sidebar.slider('DATE MINI CHOISIE',min_value=start_year,max_value=end_year, disabled=False)
    liste_columns = ['F2','A1','I1','I2','R1','R2']
    data_numbers = df_selected_year[liste_columns][df_selected_year.Year >= selection_dates_input]
    data_numbers.replace({True:1,False:0},inplace=True)
    fig7 = go.Figure()
    fig7.add_trace(go.Heatmap(
            x=liste_columns,
            z=data_numbers,
            colorscale = 'Temps', #'rdylgn'
            showscale=False
            #text=data_numbers,
            #texttemplate="%{text}",
            #textfont={"size":20}
            ))
    fig7.update_layout(
            title='Matrice FAIR',
            width=1000,
            height=1000)
    st.plotly_chart(fig7,use_container_width=True)

