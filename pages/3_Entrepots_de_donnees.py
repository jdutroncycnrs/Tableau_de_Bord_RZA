import streamlit as st
from PIL import Image
import pandas as pd
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi
import glob
import datetime
import plotly.express as px
import plotly.graph_objects as go
import requests


from Recuperation_dataverses import Recup_dataverses, Recup_contenu_dataverse,Recup_contenu, Recup_contenu_dryad, Recup_contenu_zenodo,Recup_contenu_gbif, Recup_dataverses_rdg, recuperation_zenodo, recuperation_nakala, recuperation_dryad, recuperation_gbif

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Autres entrepôts",
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

# Paramètres visuels
couleur_subtitles = (250,150,150)
taille_subtitles = "25px"
couleur_subsubtitles = (60,150,160)
taille_subsubtitles = "25px"
couleur_True = (0,200,0)
couleur_False = (200,0,0)
wch_colour_box = (250,250,220)
wch_colour_font = (90,90,90)
fontsize = 70

colors = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0','#F9A2BF','#3E9399','#3D4A81','#ECDCC5','#D2CFC8','grey','grey','grey']
graph_title_font = 24
graph_xaxis_ticks_font = 15
graph_xaxis_title_font = 20
graph_yaxis_ticks_font = 15
graph_yaxis_title_font = 20
legend_title_font = 15
legend_font =15
graph_title_color = "gray"
graph_ticks_color = 'gray'


##########################  VARIABLES DE CONNEXION #######################

######################## Data Indores ############################################
BASE_URL="https://data.indores.fr"
API_TOKEN="19f0769d-564f-44ac-809b-22853f186960"

######################## RDG ############################################
BASE_URL="https://entrepot.recherche.data.gouv.fr/"
API_TOKEN="b02fd46a-2fb0-4ac3-8717-ae70ec35185a"

######################## Nakala ############################################
url_nakala = "https://api.nakala.fr/search"
headers_nakala = {
  'X-API-KEY': 'c3cac1e9-cecc-a05c-bf8e-2459669a1f31',
  'accept': 'application/json'
}

######################## Zenodo ############################################
url_zenodo = 'https://zenodo.org/api/records/'
zenodo_token = "OMMGEVUcApEKSt4JEkSK7OzpqZQPMvGKAlB2yP2MXG6APstRn2hWpiHfpjaA"
headers_zenodo = {"Content-Type": "application/json"}

########################## DRYAD #########################################
url_dryad = "https://datadryad.org/api/v2/search?"


########################## GBIF #########################################
url_gbif = "https://api.gbif.org/v1/dataset?"
headers_gbif = {'accept': 'application/json'}


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

liste_ZAs_bis = [['Zone atelier territoires uranifères','36'],
              [' Zone Atelier Seine','37'],
              [' Zone atelier Loire','38'],
              [' Zone atelier bassin du Rhône','39'],
              [' Zone atelier bassin de la Moselle','40'],
              [' Zone atelier Alpes','42'],
              [' Zone atelier arc jurassien','43'],
              [' Zone atelier Armorique','44'],
              [' Zone atelier Plaine et Val de Sèvre','45'],
              [' Zone atelier environnementale urbaine','46'],
              [' Zone atelier Hwange','47'],
              [' Zone atelier Pyrénées Garonne','48'],
              [' Zone atelier Brest Iroise','49'],
              [' Zone Atelier Antarctique et Terres Australes','10295'],
              [' Zone Atelier Santé Environnement Camargue','10296'],
              [' Zone Atelier Argonne','10297']]

d = datetime.date.today()

all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)


###################### CREATION CONNEXION ##############################
Choix_entrepot = st.sidebar.subheader('Entrepôts')
with st.sidebar:
    if 'indores' not in st.session_state:
        st.session_state.indores = False
    if 'rdg' not in st.session_state:
        st.session_state.rdg = False
    if 'nakala' not in st.session_state:
        st.session_state.nakala = False
    if 'zenodo' not in st.session_state:
        st.session_state.zenodo = False
    if 'dryad' not in st.session_state:
        st.session_state.dryad = False
    if 'gbif' not in st.session_state:
        st.session_state.gbif = False


# Function to handle checkbox1 change
    def handle_checkbox1_change():
        if st.session_state.indores:
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.zenodo = False
            st.session_state.nakala = False
            st.session_state.zenodo = False

    # Function to handle checkbox1 change
    def handle_checkbox2_change():
        if st.session_state.rdg:
            st.session_state.indores = False
            st.session_state.nakala = False
            st.session_state.zenodo = False
            st.session_state.nakala = False
            st.session_state.zenodo = False
            

    # Function to handle checkbox2 change
    def handle_checkbox3_change():
        if st.session_state.nakala:
            st.session_state.indores = False
            st.session_state.rdg = False
            st.session_state.zenodo = False
            st.session_state.dryad = False
            st.session_state.gbif = False

    def handle_checkbox4_change():
        if st.session_state.zenodo:
            st.session_state.indores = False
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.dryad = False
            st.session_state.gbif = False
    
    def handle_checkbox5_change():
        if st.session_state.dryad:
            st.session_state.indores = False
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.gbif = False
            st.session_state.zenodo = False
    
    def handle_checkbox6_change():
        if st.session_state.gbif:
            st.session_state.indores = False
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.dryad = False
            st.session_state.zenodo = False

    choix_groupe_OHM = False
    indores = st.checkbox("INDORES", key='indores', on_change=handle_checkbox1_change)
    rdg = st.checkbox("RGD", key='rdg', on_change=handle_checkbox2_change)
    nakala = st.checkbox("NAKALA", key='nakala', on_change=handle_checkbox3_change)
    zenodo = st.checkbox("ZENODO", key='zenodo', on_change=handle_checkbox4_change)
    dryad = st.checkbox("DRYAD", key='dryad', on_change=handle_checkbox5_change)
    gbif = st.checkbox("GBIF", key='gbif', on_change=handle_checkbox6_change)

if indores:
    ######################  TITRES  #######################################
    st.title(":grey[Analyse des dépôts dans Data.InDoRes]")

    adresse_dataInDoRes = 'https://data.indores.fr/dataverse/dataindores'
    s_adresse_dataInDoRes = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_dataInDoRes}</p>"
    st.markdown(s_adresse_dataInDoRes ,unsafe_allow_html=True)

    fichier = f'tableau_dataverses-{d}.csv'

    fi = glob.glob(f"pages/data/tableau_dataverses*.csv")

    ###################### CREATION CONNEXION ##############################

    def connect_to_dataverse(BASE_URL, API_TOKEN):
        try:
            # Create a new API connection
            api = NativeApi(BASE_URL, API_TOKEN)
            resp = api.get_info_version()
            response = resp.json()
            
            # Check connection success
            if response['status']=='OK':
                st.session_state['dataverse_api'] = api
                st.success("Connexion établie avec Data. InDoRES")
            else:
                st.error("Connexion échouée!")
        except Exception as e:
            st.error(f"Connection error: {e}")
        return api
    
    ###################### Indices des dataverses ##############################

    def find_indices(lst, elements):
        indices = []
        for element in elements:
            try:
                indices.append(lst.index(element))
            except ValueError:
                pass  # Element not found in the list
        return indices

    
    ###############################################################################################
    ########### POUR L'ADMINISTRATEUR ############################################################
    ###############################################################################################

    # Mot de passe pour faire des récupérations automatisées
    admin_pass = 'admin'
    admin_action = st.sidebar.text_input(label="Pour l'administrateur")


    if admin_action == admin_pass:

        # MAJ DES ENTREPOTS EXISTANTS ##########################################
        b1 = st.sidebar.button(label=" Mise à jour des entrepôts Dataverses dans Data.InDoRes ")

        if b1==True:
            with st.spinner("Récupération des entrepôts existants"):
                api = connect_to_dataverse(BASE_URL,  API_TOKEN)
                Recup_dataverses(api,fichier)


        # RECUPERATION DES CONTENUS VIA BOUTON ##########################################       
        Recup_globale = st.sidebar.button('recupération des contenus')
        if Recup_globale:
            ids = find_indices(liste_ZAs_, Selection_ZA)
            with st.spinner("La récup globale est en cours"):
                api = connect_to_dataverse(BASE_URL,  API_TOKEN)
                liste_columns_df_entrepot=['selection','Entrepot','ID','Url','Date de publication','Titre','Auteur','Organisation',"Email",'Résumé','Thème','Publication URL']
                df_entrepot = pd.DataFrame(columns=liste_columns_df_entrepot)
                for i, za in enumerate(Selection_ZA):
                    s = liste_ZAs_bis[ids[i]][1]
                    df = Recup_contenu(api, s, za)
                    dfi = pd.concat([df_entrepot,df], axis=0)
                    dfi.reset_index(inplace=True)
                    dfi.drop(columns='index', inplace=True)
                    df_entrepot = dfi
                df_entrepot.to_csv("pages/data/Contenu_DataInDoRES2.csv")

    ############################################################################

    df_complet = pd.read_csv("pages/data/Contenu_DataInDoRES2.csv",index_col=[0])

    with st.container(border=True):
        Nombre_depots = df_complet['Entrepot'].value_counts()
        for i in range(len(liste_ZAs_)):
            if liste_ZAs_[i] in Nombre_depots.index.values:
                pass
            else:
                Nombre_depots[liste_ZAs_[i]]=0
        df = pd.DataFrame(Nombre_depots.values,index=Nombre_depots.index.values,columns=['Nombre_dépôts'])
        fig0= go.Figure()
        for i, za in enumerate(df.index.values):
            selec = df.index.values[i:i+1]
            selec_len = df['Nombre_dépôts'].values[i:i+1]
            fig0.add_trace(go.Bar(
                            y=selec,
                            x=selec_len,
                            name=za,
                            orientation = 'h',
                            marker=dict(color=colors[i])
                        ))
        fig0.update_layout(
                            title=dict(
                                    text=f'Nombre de dépôts répertoriées',
                                    font=dict(size=graph_title_font, family='Arial', color=graph_title_color)
                                    ),
                            yaxis=dict(
                                    tickfont=dict(size=graph_yaxis_ticks_font, family='Arial', color=graph_ticks_color)   
                                    ),
                                    xaxis=dict(
                                        tickfont=dict(size=graph_xaxis_ticks_font, family='Arial', color=graph_ticks_color)   
                                    ),
                                    width=1000,
                                    height=600,
                                    showlegend=False)
        st.plotly_chart(fig0,use_container_width=True)

    if len(Selection_ZA)!=0:
        df_visu = df_complet[df_complet['Entrepot'].isin(Selection_ZA)]
        df_visu.reset_index(inplace=True)
        df_visu.drop(columns='index', inplace=True)
        #st.dataframe(df_visu)

        if len(Selection_ZA)==1:
            col1,col2 = st.columns([0.7,0.3])
            with col1:
                Visu_depots = f"Données publiées dans la {Selection_ZA[0]}"
                s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
                st.markdown(s_Visu_depots ,unsafe_allow_html=True)
            with col2:
                st.metric(label="Nombre de dépôts décomptés", value=len(df_visu))
        elif 1<len(Selection_ZA)<16:
            col1,col2 = st.columns([0.7,0.3])
            with col1:
                Visu_depots = f"Données publiées dans les ZA suivantes: {Selection_ZA}"
                s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
                st.markdown(s_Visu_depots ,unsafe_allow_html=True)
            with col2:
                st.metric(label="Nombre de dépôts décomptés", value=len(df_visu))
        elif len(Selection_ZA)==16:
            col1,col2 = st.columns([0.7,0.3])
            with col1:
                Visu_depots = f"Données publiées dans l'ensemble du réseau des Zones Ateliers"
                s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
                st.markdown(s_Visu_depots ,unsafe_allow_html=True)
            with col2:
                st.metric(label="Nombre de dépôts décomptés", value=len(df_visu))
        
        if len(df_visu)!=0:
                for i in range(len(df_visu)):
                    with st.container(border=True):
                        t0 = f"FICHIER #{i+1}"
                        s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                        st.markdown(s_t0,unsafe_allow_html=True)
                        col1,col2, col3 = st.columns([0.6,0.2,0.2])
                        with col1:
                            t0a = 'Titre'
                            s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                            st.markdown(s_t0a,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Titre'])
                        with col2:
                            t0b = 'Thème'
                            s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                            st.markdown(s_t0b,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Thème'])
                        with col3:
                            t0c = 'Date'
                            s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                            st.markdown(s_t0c,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Date de publication'])
                        col1,col2, col3 = st.columns([0.6,0.2,0.2])
                        with col1:
                            t0d = 'Résumé'
                            s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                            st.markdown(s_t0d,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Résumé'])
                        with col2:
                            t0e = 'Publication URL'
                            s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                            st.markdown(s_t0e,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Publication URL'])
                        with col3:
                            t0f = 'DOI'
                            s_t0f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0f}</p>"
                            st.markdown(s_t0f,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Url'])
                        col1,col2, col3 = st.columns([0.6,0.2,0.2])
                        with col1:
                            t0g = 'Auteur'
                            s_t0g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0g}</p>"
                            st.markdown(s_t0g,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Auteur'])
                        with col2:
                            t0h = 'Organisation'
                            s_t0h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0h}</p>"
                            st.markdown(s_t0h,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Organisation'])
                        with col3:
                            t0i = 'Email'
                            s_t0i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0i}</p>"
                            st.markdown(s_t0i,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Email'])

    #############  VISU SUNBURST ###############################################

    visu_sunburst= st.sidebar.checkbox("Voir l'ensemble des entrepôts existants")

    if len(fi)!=0:
        fich = fi[-1]
        dataverses = pd.read_csv(fich)
        if visu_sunburst:
            fig = px.sunburst(dataverses, path=['niv0','niv1', 'niv2','niv3'], values='val')
            fig.update_layout(
                title=f'Visuel des différents Dataverses dans Data.InDoRes via {fich}',
                width=1000,
                height=1000)
            st.plotly_chart(fig,use_container_width=True)
    else:
        st.write('Il est nécessaire de mettre à jour vos entrepôts')


if rdg:

    ######################  TITRES  #######################################
    st.title(":grey[Analyse des dépôts dans Recherche Data Gouv]")

    adresse_RDG = 'https://entrepot.recherche.data.gouv.fr/dataverse/root?q='
    s_adresse_RDG = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_RDG}</p>"
    st.markdown(s_adresse_RDG ,unsafe_allow_html=True)

    ######################  PARAMETRES  #######################################

    fichier = f'tableau_dataverses_rdg-{d}.csv'

    fi = glob.glob(f"pages/data/rechercheDataGouv/tableau_dataverses*.csv")

    if len(fi)!=0:
        fich = fi[-1]
        dataverses = pd.read_csv(fich,index_col=[0])
    else:
        st.write('Il est nécessaire de mettre à jour vos entrepôts')


    ###################### CREATION CONNEXION ##############################
    def connect_to_dataverse(BASE_URL, API_TOKEN):
        try:
            # Create a new API connection
            api = NativeApi(BASE_URL, API_TOKEN)
            resp = api.get_info_version()
            response = resp.json()
                
            # Check connection success
            if response['status']=='OK':
                st.session_state['rdg_api'] = api
                st.success("Connexion établie avec Recherche Data Gouv")
            else:
                st.error("Connexion échouée!")
        except Exception as e:
            st.error(f"Connection error: {e}")
        return api

     #############  VISU TABLEAU  OU SUNBURST ###############################################

    if 'tab' not in st.session_state:
        st.session_state.tab = False
    if 'sun' not in st.session_state:
        st.session_state.sun = False

    def handle_tab_change():
        if st.session_state.tab:
            st.session_state.sun = False
            

    # Function to handle checkbox2 change
    def handle_sunburst_change():
        if st.session_state.sun:
            st.session_state.tab = False


    col1,col2 = st.columns(2)
    with col1:
        tab = st.checkbox("Filtrer le contenu d'un entrepôt", key='tab', on_change=handle_tab_change)
    with col2:
        sun = st.checkbox("Voir le sunburst des entrepôts", key='sun', on_change=handle_sunburst_change)


    if tab:
        dataverses['niv1-niv2']=dataverses['niv1']+' / '+dataverses['niv2']
        Selected_entrepot = st.selectbox('Choisissez votre entrepôt dans la liste', dataverses['niv1-niv2'].values)
        api_rdg = connect_to_dataverse(BASE_URL,  API_TOKEN)
        with st.spinner("Analyse en cours"):
            liste_columns_df_entrepot_rdg_selected=['selection','Entrepot','Dataverse','ID','Url','Date de publication','Titre','Auteur','Organisation',"Email",'Résumé','Thème','Publication URL', 'Check']
            df_entrepot_rdg_selected = pd.DataFrame(columns=liste_columns_df_entrepot_rdg_selected)
            s = int(dataverses['ids_niv2'][dataverses['niv1-niv2']==Selected_entrepot])
            df = Recup_contenu(api_rdg, s, Selected_entrepot, Selection_ZA[0])
            dfi = pd.concat([df_entrepot_rdg_selected,df], axis=0)
            dfi.reset_index(inplace=True)
            dfi.drop(columns='index', inplace=True)
            df_entrepot_rdg_selected = dfi
            df_entrepot_rdg_selected_ = df_entrepot_rdg_selected[df_entrepot_rdg_selected['Check']==True]
            df_entrepot_rdg_selected_.to_csv(f"pages/data/rechercheDataGouv/Contenu_RDG_{Selection_ZA[0]}_{Selected_entrepot.replace(' ','_').replace('/','_')}.csv")
        st.dataframe(df_entrepot_rdg_selected_,use_container_width=True)

    if sun:
        fig = px.sunburst(dataverses, path=['niv0','niv1','niv2'], values='val')
        fig.update_layout(
                    title=f'Visuel des différents Dataverses dans RDG via {fich}',
                    width=1000,
                    height=1000)
        st.plotly_chart(fig,use_container_width=True)


    ########## POUR L'ADMINISTRATEUR ########################################
    admin_pass = 'admin'
    admin_action = st.sidebar.text_input(label="Pour l'administrateur")

    if admin_action == admin_pass:

        b1 = st.sidebar.button(label=" Mise à jour des entrepôts Dataverses dans RDG ")

        if b1==True:
            with st.spinner("Récupération des entrepôts existants"):
                api_rdg = connect_to_dataverse(BASE_URL,  API_TOKEN)
                Recup_dataverses_rdg(api_rdg,fichier)

    # RECUPERATION DES CONTENUS VIA BOUTON ##########################################       
        Recup_globale = st.sidebar.button('recupération des contenus')
        if Recup_globale:
            with st.spinner("La récup globale est en cours"):
                api_rdg = connect_to_dataverse(BASE_URL,  API_TOKEN)
                liste_columns_df_entrepot_rdg=['selection','Entrepot','Store','ID','Url','Date de publication','Titre','Auteur','Organisation',"Email",'Résumé','Thème','Publication URL']
                df_entrepot_rdg = pd.DataFrame(columns=liste_columns_df_entrepot_rdg)
                for i in range(len(dataverses)):
                    print(i)
                    for j in range(len(Selection_ZA)):
                        print(j)
                        try:
                            s = int(dataverses.loc[i,'ids_niv2'])
                            entrepot = dataverses.loc[i,'niv2']
                            df = Recup_contenu(api_rdg, s, entrepot, Selection_ZA[j])
                            dfi = pd.concat([df_entrepot_rdg,df], axis=0)
                            dfi.reset_index(inplace=True)
                            dfi.drop(columns='index', inplace=True)
                            dfi_ = dfi[dfi['Check']==True]
                            df_entrepot_rdg = dfi_
                        except:
                            pass
                        
                df_entrepot_rdg.to_csv("pages/data/rechercheDataGouv/Contenu_RDG_complet.csv")

    ############################################################################

if nakala:
    st.title(":grey[Analyse des dépôts dans Nakala]")

    adresse_nakala = url_nakala
    s_adresse_nakala = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_nakala}</p>"
    st.markdown(s_adresse_nakala ,unsafe_allow_html=True)

    s = " ZA alpes"
    params_nakala = {'q': f'{s}'}
    r = recuperation_nakala(url_nakala,params_nakala, headers_nakala, s)
    st.write(r)

if zenodo:
    st.title(":grey[Analyse des dépôts dans Zenodo]")

    adresse_zenodo = url_zenodo
    s_adresse_zenodo = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_zenodo}</p>"
    st.markdown(s_adresse_zenodo ,unsafe_allow_html=True)

    with st.spinner("Recherche en cours"):
        liste_columns = ['Store','Entrepot','ID','Titre']
        df_global_zenodo = pd.DataFrame(columns=liste_columns)
        for i, s in enumerate(Selection_ZA):
            params_zenodo = {'q': s,
                    'access_token': zenodo_token}
            df = Recup_contenu_zenodo(url_zenodo,params_zenodo, headers_zenodo, s)
            dfi = pd.concat([df_global_zenodo,df], axis=0)
            dfi.reset_index(inplace=True)
            dfi.drop(columns='index', inplace=True)
            df_global_zenodo = dfi
        df_global_zenodo.sort_values(by='ID', inplace=True, ascending=False)
        df_global_zenodo.reset_index(inplace=True)
        df_global_zenodo.drop(columns='index', inplace=True)

    if len(df_global_zenodo)==0:
        st.metric(label="Nombre de publications trouvées", value=len(df_global_zenodo))
    else:
        st.metric(label="Nombre de publications trouvées", value=len(df_global_zenodo))
        #st.table(df_global_zenodo)
        #df_global_zenodo.to_csv("pages/data/Zenodo/Contenu_ZENODO_complet.csv")

        df_visu_zenodo = df_global_zenodo[df_global_zenodo['Entrepot'].isin(Selection_ZA)]
        df_visu_zenodo.reset_index(inplace=True)
        df_visu_zenodo.drop(columns='index', inplace=True)

        for i in range(len(df_visu_zenodo)):
            with st.container(border=True):
                t0 = f"FICHIER #{i+1}"
                s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                st.markdown(s_t0,unsafe_allow_html=True)
                col1,col2 = st.columns([0.8,0.2])
                with col1:
                    t0a = 'Titre'
                    s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                    st.markdown(s_t0a,unsafe_allow_html=True)
                    st.markdown(df_visu_zenodo.loc[i,'Titre'])
                with col2:
                    t0b = 'ID'
                    s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                    st.markdown(s_t0b,unsafe_allow_html=True)
                    st.markdown(df_visu_zenodo.loc[i,'ID'])

if dryad:
    st.title(":grey[Analyse des dépôts dans Dryad]")

    adresse_dryad = url_dryad
    s_adresse_dryad = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_dryad}</p>"
    st.markdown(s_adresse_dryad ,unsafe_allow_html=True)

    with st.spinner("Recherche en cours"):
        liste_columns_dryad = ['Store','Entrepot','ID','Date de publication','Titre','Auteur prénom 1','Auteur Nom 1',
                            'Organisation 1',"Email 1",'Auteur prénom 2','Auteur Nom 2','Organisation 2',"Email 2",
                            'Auteur prénom 3','Auteur Nom 3','Organisation 3',"Email 3",'Résumé','Thème','Publication URL']
        df_dryad_global = pd.DataFrame(columns=liste_columns_dryad)
        for i in range(len(Selection_ZA)):
            params_dryad = {'q':Selection_ZA[i]}
            Nombre_dryad, df_dryad = Recup_contenu_dryad(url_dryad,params_dryad, Selection_ZA[i])
            dfi = pd.concat([df_dryad_global,df_dryad], axis=0)
            dfi.reset_index(inplace=True)
            dfi.drop(columns='index', inplace=True)
            df_dryad_global = dfi

        df_dryad_global.sort_values(by='Date de publication', inplace=True, ascending=False)
        df_dryad_global.reset_index(inplace=True)
        df_dryad_global.drop(columns='index', inplace=True)
    
    if len(df_dryad_global)==0:
        st.metric(label="Nombre de publications trouvées", value=len(df_dryad_global))
    else:
        st.metric(label="Nombre de publications trouvées", value=len(df_dryad_global))
        #st.dataframe(df_dryad_global,use_container_width=True)
        #df_dryad_global.to_csv("pages/data/Dryad/Contenu_DRYAD_complet.csv")

        df_visu_dryad = df_dryad_global[df_dryad_global['Entrepot'].isin(Selection_ZA)]
        df_visu_dryad.reset_index(inplace=True)
        df_visu_dryad.drop(columns='index', inplace=True)

        for i in range(len(df_visu_dryad)):
            with st.container(border=True):
                t0 = f"FICHIER #{i+1}"
                s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                st.markdown(s_t0,unsafe_allow_html=True)
                col1,col2, col3 = st.columns([0.6,0.2,0.2])
                with col1:
                    t0a = 'Titre'
                    s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                    st.markdown(s_t0a,unsafe_allow_html=True)
                    st.markdown(df_visu_dryad.loc[i,'Titre'])
                with col2:
                    t0b = 'Thème'
                    s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                    st.markdown(s_t0b,unsafe_allow_html=True)
                    st.markdown(df_visu_dryad.loc[i,'Thème'])
                with col3:
                    t0c = 'Date'
                    s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                    st.markdown(s_t0c,unsafe_allow_html=True)
                    st.markdown(df_visu_dryad.loc[i,'Date de publication'])
                col1,col2 = st.columns([0.6,0.4])
                with col1:
                    t0d = 'Résumé'
                    s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                    st.markdown(s_t0d,unsafe_allow_html=True)
                    st.markdown(df_visu_dryad.loc[i,'Résumé'])
                with col2:
                    t0e = 'Publication URL'
                    s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                    st.markdown(s_t0e,unsafe_allow_html=True)
                    st.markdown(df_visu_dryad.loc[i,'Publication URL'])
                col1,col2, col3 = st.columns([0.6,0.2,0.2])
                with col1:
                    t0g = 'Auteur'
                    s_t0g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0g}</p>"
                    st.markdown(s_t0g,unsafe_allow_html=True)
                with col2:
                    t0h = 'Organisation'
                    s_t0h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0h}</p>"
                    st.markdown(s_t0h,unsafe_allow_html=True)
                with col3:
                    t0i = 'Email'
                    s_t0i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0i}</p>"
                    st.markdown(s_t0i,unsafe_allow_html=True)
                for b in range(3):
                    with col1:
                        st.markdown(f"{df_visu_dryad.loc[i,f'Auteur Nom {b+1}']} , {df_visu_dryad.loc[i,f'Auteur prénom {b+1}']}")
                    with col2:
                        st.markdown(df_visu_dryad.loc[i,f'Organisation {b+1}'])
                    with col3:
                        st.markdown(df_visu_dryad.loc[i,f'Email {b+1}'])


if gbif:
    st.title(":grey[Analyse des dépôts dans GBIF]")

    adresse_gbif = url_gbif
    s_adresse_gbif = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_gbif}</p>"
    st.markdown(s_adresse_gbif ,unsafe_allow_html=True)

    with st.spinner("Recherche en cours"):
        liste_columns_gbif = ['Store','Entrepot','ID','Date de publication','Titre','Auteur prénom 1','Auteur Nom 1',
                                'Organisation 1',"Email 1",'Résumé','Publication URL']
        df_gbif_global = pd.DataFrame(columns=liste_columns_gbif)
        for i in range(len(Selection_ZA)):
            params_gbif = {'q':Selection_ZA[i],
                            'limit':1000}
            df_gbif = Recup_contenu_gbif(url_gbif,params_gbif,headers_gbif,Selection_ZA[i])
            dfi = pd.concat([df_gbif_global,df_gbif], axis=0)
            dfi.reset_index(inplace=True)
            dfi.drop(columns='index', inplace=True)
            df_gbif_global = dfi

        df_gbif_global.sort_values(by='Date de publication', inplace=True, ascending=False)
        df_gbif_global.reset_index(inplace=True)
        df_gbif_global.drop(columns='index', inplace=True)
        df_gbif_global['Date de publication 2'] = pd.to_datetime(df_gbif_global['Date de publication']).dt.strftime('%Y-%m-%d')

    df_gbif_global.to_csv("pages/data/Gbif/Contenu_GBIF_complet.csv")

    if len(df_gbif_global)==0:
        st.metric(label="Nombre de publications trouvées", value=len(df_gbif_global))
    else:
        st.metric(label="Nombre de publications trouvées", value=len(df_gbif_global))
        #st.dataframe(df_gbif_global)

        df_visu_gbif = df_gbif_global[df_gbif_global['Entrepot'].isin(Selection_ZA)]
        df_visu_gbif.reset_index(inplace=True)
        df_visu_gbif.drop(columns='index', inplace=True)

        for i in range(len(df_visu_gbif)):
            with st.container(border=True):
                t0 = f"FICHIER #{i+1}"
                s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                st.markdown(s_t0,unsafe_allow_html=True)
                col1,col2 = st.columns([0.8,0.2])
                with col1:
                    t0a = 'Titre'
                    s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                    st.markdown(s_t0a,unsafe_allow_html=True)
                    st.markdown(df_visu_gbif.loc[i,'Titre'])
                with col2:
                    t0c = 'Date'
                    s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                    st.markdown(s_t0c,unsafe_allow_html=True)
                    st.markdown(df_visu_gbif.loc[i,'Date de publication 2'])
                col1,col2 = st.columns([0.6,0.4])
                with col1:
                    t0d = 'Résumé'
                    s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                    st.markdown(s_t0d,unsafe_allow_html=True)
                    st.markdown(df_visu_gbif.loc[i,'Résumé'])
                with col2:
                    t0e = 'Publication URL'
                    s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                    st.markdown(s_t0e,unsafe_allow_html=True)
                    st.markdown(df_visu_gbif.loc[i,'Publication URL'])
                col1,col2, col3 = st.columns([0.6,0.2,0.2])
                with col1:
                    t0g = 'Auteur'
                    s_t0g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0g}</p>"
                    st.markdown(s_t0g,unsafe_allow_html=True)
                with col2:
                    t0h = 'Organisation'
                    s_t0h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0h}</p>"
                    st.markdown(s_t0h,unsafe_allow_html=True)
                with col3:
                    t0i = 'Email'
                    s_t0i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0i}</p>"
                    st.markdown(s_t0i,unsafe_allow_html=True)
                for b in range(1):
                    with col1:
                        st.markdown(f"{df_visu_gbif.loc[i,f'Auteur Nom {b+1}']} , {df_visu_gbif.loc[i,f'Auteur prénom {b+1}']}")
                    with col2:
                        st.markdown(df_visu_gbif.loc[i,f'Organisation {b+1}'])
                    with col3:
                        st.markdown(df_visu_gbif.loc[i,f'Email {b+1}'])