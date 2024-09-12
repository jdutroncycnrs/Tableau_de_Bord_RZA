import streamlit as st
import pandas as pd
import datetime
import glob
import requests
import json
import re
import numpy as np
import plotly.express as px
import time
from Recuperation_uuids import scraping_GN, uuids_cleaning, recup_group
from Traitement_records import transcript_json, recup_fiche

###############################################################################
########### TITRE ET CONFIG  DE L'ONGLET ######################################
###############################################################################
st.set_page_config(
    page_title="Analyse des fiches de métadonnées du GeoNetwork",
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

###############################################################################
############ PARAMETRES INSTANCIES #######################################################
###############################################################################

# Date du jour
d = datetime.date.today()
# url du geonetwork
url = "https://cat.indores.fr/geonetwork/srv/api/records/"

# Accès au geonetwork
headers_json = {"accept":"application/json",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}
headers_xml = {"accept":"application/xml",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}
headers_text = {"accept":"text/plain",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}

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

# Listes
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
             'RZA',
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

filtre_mention =['ZAA','zaa ','Zone Atelier Alpes', 'ZAA - Alpes',
           'ZAAJ','Zone Atelier Arc Jurassien' , 'ZAAJ - Arc Jurassien', 'Jura',
           'ZAAR','zaar', 'Zone Atelier Armorique','ZAAr - Armorique','ZAAr',
           'ZAEU','zaeu','Zone atelier environnementale urbaine','ZAEU - Environnementale Urbaine',
           'ZABR','zabr','Zone atelier bassin du Rhône','ZABR - Bassin du Rhône',
           'ZABRI','zabri','Zone atelier Brest Iroise','ZABrI - Brest Iroise',
           'ZAM','zam','Zone atelier bassin de la Moselle', 'ZAM - Moselle',
           'ZAL','zal','Zone atelier Loire','ZAL - Loire',
           'ZAS','zas','Zone Atelier Seine', 'ZAS - Seine',
           'ZAPygar','Zone atelier Pyrénées Garonne', 'ZAPYGAR - Pyrénées-Garonne'
           'ZACAM','Zone Atelier Santé Environnement Camargue', 'ZACAM - Sante Environnement Camargue',
           'ZATU','Zone atelier territoires uranifères', 'ZATU - Territoires Uranifères',
           'ZATA','Zone Atelier Antarctique et Terres Australes',
           'ZARG','Zone Atelier Argonne', 'ZARG - Argonne',
           'ZAPVS','Zone atelier Plaine et Val de Sèvre', 'ZAPVS - Plaine et Val de Sèvre',
           'ZAH', 'Zone Atelier Hwange', 'ZAHV - Hwange',
           'OHMi Nunavik', 'OHM Oyapock', 'OHM Pays de Bitche', 'OHM Bassin Minier de Provence', 
           'OHMi Téssékéré', 'OHM Vallée du Rhône','OHMi Estarreja','OHM Pyrénées - haut Vicdessos', 
           'OHM Littoral méditerranéen', 'OHMi Pima County', 'OHM Littoral Caraïbe']

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

###############################################################################################
############## RECUPERATION DES IDENTIFIANTS EXISTANTS ########################################

# Besoin de récupérer l'ensemble des identifiants

# On scanne pour savoir si un fichier existe
fi = glob.glob(f"pages/data/uuids/uuid_cat_InDoRes_clean*.csv")

st.title(':grey[Visualisation des fiches]')

# Si oui, on récupère le dernier enregistré ; si non, on récupère les identifiants à la date donnée
if len(fi)!=0:
    fichier_uuids = fi[-1]
    derniere_date_recup = f"Dernière date de récupération des identifiants: {fichier_uuids[40:-4]}"
    s_derniere_date_recup  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{derniere_date_recup}</p>"
    st.markdown(s_derniere_date_recup ,unsafe_allow_html=True)
    ############################## UUIDS ########################################
    uuids = pd.read_csv(fichier_uuids, index_col=[0])
else:
    with st.spinner("Connexion au GeoNetwork et récupération des identifiants existants"):
        try:
            scraping_GN(d)
            uuids_cleaning(d)
            st.experimental_rerun()
        except:
            st.write('Il est impossible de récupérer les identifiants') 
        

#######################################################################################################
############## MAPPING GROUPES ET TABLEAU GLOBAL ######################################################

group_mentions = pd.read_csv("pages/data/infos_MD/infos_groupes_mentions.csv", index_col=[0])
tableau = pd.read_csv("pages/data/infos_MD/Tableau_MD.csv", index_col=[0])

group_mentions['Groupe_et_Mention'] = group_mentions['Groupe_et_Mention'].map(dico)
tableau['Groupe_et_Mention'] = tableau['Groupe_et_Mention'].map(dico)

##################### SELECTION ########################################################################
########### Choix OHM/RZA ##############################################################################
## Le choix est exclusif ###############################################################################
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


if checkbox1:
    selection_group = st.sidebar.multiselect('choix du groupe',options=liste_ZAs)
    if len(selection_group)==0:
        selection_group = liste_ZAs 
    selected_uuids = group_mentions['Identifiant'][group_mentions['Groupe_et_Mention'].isin(selection_group)]
    selected_uuids_ = selected_uuids.reset_index(drop=True)
    st.sidebar.metric('Nombre de fiches:',len(selected_uuids_))
elif checkbox2:
    selection_group = st.sidebar.multiselect('choix du groupe',options=liste_OHMs)
    if len(selection_group)==0:
        selection_group = liste_OHMs
    selected_uuids = group_mentions['Identifiant'][group_mentions['Groupe_et_Mention'].isin(selection_group)]
    selected_uuids_ = selected_uuids.reset_index(drop=True)
    st.sidebar.metric('Nombre de fiches:',len(selected_uuids_))
else:
    selected_uuids_ = group_mentions['Identifiant']
    st.sidebar.metric('Nombre de fiches:',len(selected_uuids_))

##################################################################################################
########## TITRE DE LA PAGE ######################################################################
#title = "Visualisation des fiches"
#s_title = f"<p style='font-size:50px;color:rgb(140,140,140)'>{title}</p>"
#st.markdown(s_title,unsafe_allow_html=True)

if 'count' not in st.session_state:
    st.session_state.count = 0
def increment_counter():
    st.session_state.count += 1
def reset_counter():
    st.session_state.count = 0

with st.container(border=True):
    s1 = "IDENTIFIEUR"
    s_s1 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s1}</p>"
    st.markdown(s_s1,unsafe_allow_html=True)

    if st.session_state.count > len(selected_uuids_):
        st.session_state.count = 0

    id_choisie = selected_uuids_[0]
    col01,col02,col03,col4 = st.columns([0.7,0.1,0.1,0.1])
    with col01:
        try:
            identifieur = st.selectbox(label='',options=selected_uuids_, index=st.session_state.count)
        except: 
            identifieur = ""
            reset_counter()
    with col02:
        st.markdown('')
        st.markdown('')
        button1 = st.button(':heavy_plus_sign:',on_click=increment_counter)
    with col03:
        st.markdown('')
        st.markdown('')
        button2 =st.button('R',on_click=reset_counter)
    with col4:
        st.metric(label="compteur",value=st.session_state.count)

    if st.session_state.count > len(selected_uuids_):
        st.write('Vous êtes au bout!')


##################################################################################################
########## CONNEXION AU GEONETWORK ###############################################################

try:
    if 'oai:search-data.ubfc.fr:' in identifieur:
        identifieur = identifieur.replace('oai:search-data.ubfc.fr:','zaaj_')
        df = pd.read_csv(f'pages/data/fiches_csv/{identifieur}.csv',index_col=[0])
        F1 = True
        F1c = couleur_True
        A2 = True
        A2c = couleur_True
    else:
        df = pd.read_csv(f'pages/data/fiches_csv/{identifieur}.csv',index_col=[0])
        F1 = True
        F1c = couleur_True
        A2 = True
        A2c = couleur_True
except:
    if 'zaaj_' in identifieur:
        identifieur = identifieur.replace('zaaj_','oai:search-data.ubfc.fr:')
    url_ = url + identifieur
    resp1 = requests.get(url_,headers=headers_json)
    if resp1.status_code == 200:
        resp_json=resp1.json()
        try:
            if 'oai:search-data.ubfc.fr:' in identifieur:
                identifieur = identifieur.replace('oai:search-data.ubfc.fr:','zaaj_')
                with open(f"pages/data/fiches_json/{identifieur}.json", "w") as f:
                    json.dump(resp_json, f, indent=4)
            else:
                with open(f"pages/data/fiches_json/{identifieur}.json", "w") as f:
                    json.dump(resp_json, f, indent=4)
        except:
            st.markdown("Cette fiche n'est pas lisible")
     
    resp2 = requests.get(url_,headers=headers_xml)
    if resp2.status_code == 200:
        xml_content = resp2.text
        try:
            with open(f"pages/data/fiches_xml/{identifieur}.xml", 'w') as file:
                file.write(xml_content)
        except:
            pass

    url_asso = url_ +"/associated?rows=100"
    resp_asso = requests.get(url_asso,headers=headers_json)
    if resp_asso.status_code == 200:
        resp_asso_json=resp_asso.json()
        try:
            with open(f"pages/data/associated_resources/resource_{identifieur}.json", "w") as f:
                json.dump(resp_asso_json, f, indent=4)
        except:
            pass

    url_attach = url_ +"/attachments"
    resp_attach = requests.get(url_attach,headers=headers_json)
    if resp_attach.status_code == 200:
        resp_attach_json=resp_attach.json()
        try:
            with open(f"pages/data/attachments/attachments_{identifieur}.json", "w") as f:
                json.dump(resp_attach_json, f, indent=4)
        except:
            pass

#######################################################################################################
############## VERIFICATION GROUPES ###################################################################

try:
    df_infos = pd.read_csv("pages/data/infos_MD/infos_groupes.csv",index_col=[0])
except:
    df_infos = pd.DataFrame(columns=['Identifiant','Groupe'])
    df_infos.to_csv("pages/data/infos_MD/infos_groupes.csv")

if 'zaaj_' in identifieur:
    identifieur = identifieur.replace('zaaj_','oai:search-data.ubfc.fr:')

liste_id = list(df_infos.Identifiant)
if identifieur in liste_id:
    pass
else:
    try:
        g = recup_group(uuid=identifieur)
    except:
        g = ""
    d = pd.DataFrame(data = [[identifieur,g]],columns=['Identifiant','Groupe'])
    df_infos_ = pd.concat([df_infos,d], axis=0)
    df_infos = df_infos_
    df_infos.reset_index(inplace=True)
    df_infos.drop(columns='index',inplace=True)
    df_infos.to_csv("pages/data/infos_MD/infos_groupes.csv")


##################################################################################################
################ TRAITEMENT DU JSON #############################################################
try:
    if 'oai:search-data.ubfc.fr:' in identifieur:
        identifieur = identifieur.replace('oai:search-data.ubfc.fr:','zaaj_')
    with open(f"pages/data/fiches_json/{identifieur}.json", 'r') as f:
        data = json.load(f)

    with open(f'pages/data/fiches_txt/{identifieur}.txt', 'w') as file:
        transcript_json(data, file)

    with open(f'pages/data/fiches_txt/{identifieur}.txt', 'r') as f:
        d = f.read()

    listi = re.split('µ',d)

    df = pd.DataFrame(listi, columns=['Results'])
    for u in range(len(df)):
        p = re.split('§',df.loc[u,'Results'])
        try:
            df.loc[u,'Valeurs']=p[1]
        except:
            pass
        try:
            df.loc[u,'Clés']=p[0].replace('.','£')
        except:
            pass

    for j in range(len(df)):
        pp = re.split('£',df.loc[j,'Clés'])
        for k in range(15):
            try:
                df.loc[j,f'K{k}']=pp[k]
            except:
                pass
    df.to_csv(f'pages/data/fiches_csv/{identifieur}.csv')
    visu = df[['Clés','Valeurs']]
    #st.dataframe(visu, use_container_width=True)
    F1 = True
    F1c = couleur_True
    A2 = True
    A2c = couleur_True
except:
    st.write("Le processus n'a pas fonctionné")
    F1 = False
    F1c = couleur_False
    A2 = False
    A2c = couleur_False

##################################################################################################
#########  VARIABLES RECUPEREES POUR AFFICHAGE ###################################################

if "zaaj_" in identifieur:
    try:
        Langue = df['Valeurs'][df['Clés']=="dc:title£@xml:lang:"].values
    except:
        Langue = ""
else:
    try:
        Langue = df['Valeurs'][df['Clés']=="gmd:language£gco:CharacterString£#text:"].values[0]
    except:
        try:
            Langue = df['Valeurs'][df['Clés']=="gmd:language£gmd:LanguageCode£@codeListValue:"].values[0]
        except:
            Langue = ""
try:
    JeuDeCaracteres = df['Valeurs'][df['Clés']=="gmd:characterSet£gmd:MD_CharacterSetCode£@codeListValue:"].values[0]
except:
    JeuDeCaracteres =""
try:
    Type = df['Valeurs'][df['Clés']=="gmd:hierarchyLevel£gmd:MD_ScopeCode£@codeListValue:"].values[0]
except:
    try:
        Type = df['Valeurs'][df['Clés']=="gfc:featureType£gfc:FC_FeatureType£gfc:typeName£gco:LocalName£#text:"].values[0]
    except:
        try:
            Type = df['Valeurs'][df['Clés']=="dc:type£#text:"].values[0]
        except:
            Type =""
try:
    Date = df['Valeurs'][df['Clés']=="gmd:dateStamp£gco:DateTime£#text:"].values[0]
except:
    try:
        Date = df['Valeurs'][df['Clés']=="gfc:versionDate£gco:DateTime£#text:"].values[0]
    except:
        try:
            Date = df['Valeurs'][df['Clés']=="gmx:versionDate£gco:DateTime£#text:"].values[0]
        except:
            try:
                Date = df['Valeurs'][df['Clés']=="dc:date£#text:"].values[0]
            except:
                Date = ""

if 'zaaj_' in identifieur:  
    try:                      
        Standard = df['Valeurs'][df['Clés']=="@xsi:noNamespaceSchemaLocation:"].values[0]
    except:
        Standard = ""
else:
    try:
        Standard = df['Valeurs'][df['Clés']=="gmd:metadataStandardName£gco:CharacterString£#text:"].values[0]
    except:
        try:
            Standard = df['Valeurs'][df['Clés']=="gfc:name£gco:CharacterString£@xmlns:gco:"].values[0]
        except:
            Standard = ""
try:
    Version_standard = df['Valeurs'][df['Clés']=="gmd:metadataStandardVersion£gco:CharacterString£#text:"].values[0]
except:
    Version_standard = ""

if 'zaaj_' in identifieur:    
    try:                    
        Nom_contact = df['Valeurs'][df['Clés']=="dc:creator£#text:"].values
    except:
        Nom_contact = ""
else:
    try:
        Nom_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values
        if len(Nom_contact)==0:
            Nom_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values
    except:
        try:
            Nom_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values
        except:
            try:
                Nom_contact = df['Valeurs'][df['Clés']=="gfc:producer£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values[0]
            except: 
                Nom_contact = ""

if 'zaaj_' in identifieur:  
    try:                      
        Organisation_contact = df['Valeurs'][df['Clés']=="dc:publisher£#text:"].values
    except:
        Organisation_contact = ""
else:
    try:
        Organisation_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values
        if len(Organisation_contact)==0:
            Organisation_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values
    except:
        try:
            Organisation_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values
        except:
            Organisation_contact = ""
try:
    Position_contact =df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values
    if len(Position_contact)==0:
        Position_contact =df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values
except:
    try:
        Position_contact =df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values
    except:
        Position_contact = ""
try:
    Tel_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values
    if len(Tel_contact)==0:
        Tel_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values
except:
    try:
        Tel_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values
    except:
        Tel_contact = ""
try:
    DeliveryPoint = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:deliveryPoint£gco:CharacterString£#text:"].values
    if len(DeliveryPoint)==0:
        DeliveryPoint = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:deliveryPoint£gco:CharacterString£#text:"].values
except:
    try:
        DeliveryPoint = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:deliveryPoint£gco:CharacterString£#text:"].values
    except:
        DeliveryPoint = ""
try:
    CodePostal = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:postalCode£gco:CharacterString£#text:"].values
    if len(CodePostal)==0:
        CodePostal = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:postalCode£gco:CharacterString£#text:"].values
except:
    try:
        CodePostal = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:postalCode£gco:CharacterString£#text:"].values
    except:
        CodePostal = ""
try:
    Ville = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:city£gco:CharacterString£#text:"].values
    if len(Ville)==0:
        Ville = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:city£gco:CharacterString£#text:"].values
except:
    try:
        Ville = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:city£gco:CharacterString£#text:"].values
    except:
        Ville = ""
try:
    Pays = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:country£gco:CharacterString£#text:"].values
    if len(Pays)==0:
        Pays = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:country£gco:CharacterString£#text:"].values
except:
    try:
        Pays = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:country£gco:CharacterString£#text:"].values
    except:
        Pays =""
try:
    Email = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:electronicMailAddress£gco:CharacterString£#text:"].values[0]
except:
    try:
        Email = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:electronicMailAddress£gco:CharacterString£#text:"].values[0]
    except:
        Email = ""


try:
    SystemReference =  df['Valeurs'][df['Clés']=="gmd:referenceSystemInfo£gmd:MD_ReferenceSystem£gmd:referenceSystemIdentifier£gmd:RS_Identifier£gmd:code£gco:CharacterString£#text:"].values
except:
    SystemReference = ""
try:
    westBoundLongitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:westBoundLongitude£gco:Decimal£#text:"].values[0]
except:
    westBoundLongitude = ""
try:
    EastBoundLongitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:eastBoundLongitude£gco:Decimal£#text:"].values[0]
except:
    EastBoundLongitude = ""
try:
    SouthBoundLatitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:southBoundLatitude£gco:Decimal£#text:"].values[0]
except:
    SouthBoundLatitude = ""
try:
    NorthBoundLatitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:northBoundLatitude£gco:Decimal£#text:"].values[0]
except:
    NorthBoundLatitude = ""

try: 
    Titre = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:title£gco:CharacterString£#text:"].values[0]
except:
    try:
        Titre = df['Valeurs'][df['Clés']=="gfc:name£gco:CharacterString£#text:"].values[0]
    except:
        try:
            Titre = df['Valeurs'][df['Clés']=="dc:title£#text:"].values[0]
        except:
            Titre = ""
try: 
    FicheParent = df['Valeurs'][df['Clés']=="gmd:parentIdentifier£gco:CharacterString£#text:"].values[0]
except:
    FicheParent = ""

if 'zaaj_' in identifieur:
    try:
        Abstract =df['Valeurs'][df['Clés']=="dc:description£#text:"].values
    except:
        Abstract = ""
else:
    try:
        Abstract =df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:abstract£gco:CharacterString£#text:"].values[0]
    except:
        Abstract = ""

try:
    Date_creation = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:date£gco:DateTime£#text:"].values[0]
except:
    Date_creation = ""
try:
    Purpose = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:purpose£gco:CharacterString£#text:"].values[0]
except:
    Purpose = ""
try:
    Status = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:status£gmd:MD_ProgressCode£@codeListValue:"].values[0]
except:
    Status = ""
try:
    Freq_maj = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceMaintenance£gmd:MD_MaintenanceInformation£gmd:maintenanceAndUpdateFrequency£gmd:MD_MaintenanceFrequencyCode£@codeListValue:"].values[0]
except:
    Freq_maj = ""

Type_dates = []
Dates = []
try:
    for li in range(len(df)):
        if df.loc[li,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:dateType£gmd:CI_DateTypeCode£@codeListValue:":
            Type_dates.append(df.loc[li,'Valeurs'])
except:
    pass
try:
    for l in range(len(df)):
        if df.loc[l,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:date£gco:Date£#text:":
            Dates.append(df.loc[l,'Valeurs'])
except:
    pass
liste_dates = []
try:
    for da in range(len(Type_dates)):
        liste_dates.append([Type_dates[da],Dates[da]])
except:
    pass

try:
    SupplementInfo = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:supplementalInformation£gco:CharacterString£#text:"].values[0]
except:
    SupplementInfo = ""

Liste_Theme = []
Liste_Thesaurus = []
Mots_cles = []
Mots_cles_zaaj = []
if 'zaaj_' in identifieur: 
    for u in range(len(df)):
        if df.loc[u,'Clés']=="dc:subject£#text:":
            Mots_cles_zaaj.append(df.loc[u,'Valeurs'])
else:
    try:
        for u in range(len(df)):
            if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:type£gmd:MD_KeywordTypeCode£@codeListValue:":
                Liste_Theme.append([u,df.loc[u,'Valeurs']])
    except:
        pass
    try:
        for u in range(len(df)):
            if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:thesaurusName£gmd:CI_Citation£gmd:title£gco:CharacterString£#text:":
                Liste_Thesaurus.append([u,df.loc[u,'Valeurs']])
    except:
        pass
    try:
        for u in range(len(df)):
            if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:keyword£gco:CharacterString£#text:" or  df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:keyword£gmx:Anchor£#text:":
                Mots_cles.append([u,df.loc[u,'Valeurs']])
    except:
        pass

theme_thesaurus_motsCles = []
mm = 0    
for th in range(1):
    liste_mots_cles = []
    try:
        if Liste_Theme[th][0]< Liste_Thesaurus[th][0]:
            for m in range(mm,len(Mots_cles)):
                if Mots_cles[m][0]<Liste_Theme[th][0]:
                    liste_mots_cles.append(Mots_cles[m][1])
                    mm = m
            theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],Liste_Thesaurus[th][1]])
    except:
        try:
            for m in range(mm,len(Mots_cles)):
                if Mots_cles[m][0]<Liste_Theme[th][0]:
                    liste_mots_cles.append(Mots_cles[m][1])
                    mm = m
            theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],"Aucun thésaurus"])
        except:
            theme_thesaurus_motsCles.append([liste_mots_cles,"Aucun thème","Aucun thésaurus"])

for th in range(1,len(Liste_Theme)):
    liste_mots_cles = []
    try:
        if Liste_Theme[th][0]< Liste_Thesaurus[th][0]:
            for m in range(mm+1,len(Mots_cles)):
                if Mots_cles[m][0]<Liste_Theme[th][0]:
                    liste_mots_cles.append(Mots_cles[m][1])
                    mm = m
            theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],Liste_Thesaurus[th][1]])
    except:
        try:
            for m in range(mm+1,len(Mots_cles)):
                if Mots_cles[m][0]<Liste_Theme[th][0]:
                    liste_mots_cles.append(Mots_cles[m][1])
                    mm = m
            theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],"Aucun thésaurus"])
        except:
            theme_thesaurus_motsCles.append([liste_mots_cles,"Aucun thème","Aucun thésaurus"])

Thesaurus = []
for i in range(len(Liste_Thesaurus)):
    Thesaurus.append(Liste_Thesaurus[i][1])

Themes = []
for i in range(len(Liste_Theme)):
    Themes.append(Liste_Theme[i][1])

if 'zaaj_' in identifieur: 
    Keywords = Mots_cles_zaaj
else:
    Keywords = []
    for i in range(len(Mots_cles)):
        Keywords.append(Mots_cles[i][1])

mention = 'Aucune mention'
Titre_Keywords = Titre.split()
for k in Keywords:
    Titre_Keywords.append(k)

for s in Titre_Keywords:
    if s in filtre_mention:
        mention = s
    else:
        pass

try:
    UseLimitation = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:useLimitation£gco:CharacterString£#text:"].values[0]
except:
    UseLimitation =""

if 'zaaj_' in identifieur:
    try:
        UseContrainte = df['Valeurs'][df['Clés']=="dc:rights£#text:"].values
    except:
        UseContrainte =""
else:
    try:
        UseContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:useConstraints£gmd:MD_RestrictionCode£@codeListValue:"].values[0]
    except:
        UseContrainte =""
try:
    AccesContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:accessConstraints£gmd:MD_RestrictionCode£@codeListValue:"].values[0]
except:
    AccesContrainte =""
try:
    AutreContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:otherConstraints£gco:CharacterString£#text:"].values[0]
except:
    AutreContrainte =""

if 'zaaj_' in identifieur:
    try:                        
        Format = df['Valeurs'][df['Clés']=="dc:format£#text:"].values
    except:
        Format = ""
else:
    try:
        Format = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:distributionFormat£gmd:MD_Format£gmd:name£gco:CharacterString£#text:"].values
    except:
        Format = ""

if 'zaaj_' in identifieur:
    try:
        Online_links = df['Valeurs'][df['Clés']=="dc:relation£#text:"].values
    except:
        Online_links = ""
else:
    try:
        Online_links = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:linkage£gmd:URL:"].values
    except:
        Online_links = ""
try:
    Online_protocols = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:protocol£gco:CharacterString£#text:"].values
except:
    Online_protocols = ""
try:
    Online_nom = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:name£gco:CharacterString£#text:"].values
except:
    Online_nom = ""
try:
    Online_description = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:description£gco:CharacterString£#text:"].values
except:
    Online_description = ""

try:
    Niveau = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:scope£gmd:DQ_Scope£gmd:level£gmd:MD_ScopeCode£@codeListValue:"].values[0]
except:
    Niveau = ""
try:
    Conformite = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:report£gmd:DQ_DomainConsistency£gmd:result£gmd:DQ_ConformanceResult£gmd:pass£gco:Boolean£#text:"].values[0]
except:
    Conformite = ""
try:
    Genealogie = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:lineage£gmd:LI_Lineage£gmd:statement£gco:CharacterString£#text:"].values[0]
except:
    Genealogie = ""
try:
    Scope = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:scope£gmd:DQ_Scope£gmd:levelDescription£gmd:MD_ScopeDescription£gmd:attributes£#text:"].values[0]
except:
    Scope = ""

if 'zaaj_' in identifieur:
    identifieur = identifieur.replace('zaaj_','oai:search-data.ubfc.fr:')
    try:
        groupe = group_mentions['Groupe'][group_mentions.Identifiant==identifieur].values[0]
    except:
        groupe = ""

    identifieur = identifieur.replace('oai:search-data.ubfc.fr:','zaaj_')
else:
    try:
        groupe = group_mentions['Groupe'][group_mentions.Identifiant==identifieur].values[0]
    except:
        groupe = ""

##################################################################################################
######### VARIABLES EVALUATION FAIR ##############################################################

if len(Titre)!=0 and len(Abstract)!=0 and len(Organisation_contact)!=0 and len(Nom_contact)!=0 and len(Email)!=0:
    F2 = True
    F2c = couleur_True
else:
    F2 = False
    F2c = couleur_False

if len(Online_links)!=0:
    for i in range(len(Online_links)):
        if 'doi' in Online_links[i] or 'attachments' in Online_links[i]:
            A1 = True
            A1c = couleur_True
            F3 = True
            F3c = couleur_True
        else:
            A1 = False
            A1c = couleur_False
            F3 = False
            F3c = couleur_False
else:
    A1 = False
    A1c = couleur_False
    F3 = False
    F3c = couleur_False

if groupe in (['Aucun groupe', 'Groupe exemple']):
    F4 = False
    F4c = couleur_False
else:
    F4 = True
    F4c = couleur_True

if len(Format)!=0:
    for i in range(len(Format)):
        if Format[i] in ['GeoTiff','GeoTIFF', 'GEOTIFF','shape','ESRI Shapefile','Word','ASC','CSV','png','PNG','pdf','PDF','svg','SVG', 'odt','ODT','rtf', 'RTF','txt','TXT','jpg','JPG','ods','ODS','mkv','MKV','zip','ZIP','tar','TAR']:
            I1 = True
            I1c = couleur_True
        else:
            I1 = False
            I1c = couleur_False
else:
    I1 = False
    I1c = couleur_False

if len(Thesaurus)==0:
    I2 = False
    I2c = couleur_False
else:
    I2 = True
    I2c = couleur_True

if len(Keywords)==0:
    I3 = False
    I3c = couleur_False
else:
    I3 = True
    I3c = couleur_True

if len(UseLimitation)==0 and  len(UseContrainte)==0 and len(AccesContrainte)==0 and len(AutreContrainte)==0:
    R1 = False
    R1c = couleur_False
elif len(UseContrainte)!=0 or len(UseLimitation)!=0:
    R1 = True
    R1c = couleur_True
else:
    R1 = False
    R1c = couleur_False

if len(Genealogie)==0:
    R2 = False
    R2c = couleur_False
else:
    R2 = True
    R2c = couleur_True

R3 = False
R3c = couleur_False

# INFORMATIONS DE LA FICHE INDIVIDUELLE ################################################################

liste_variables = [identifieur, Langue, JeuDeCaracteres, Type, Date, Standard, Version_standard, Nom_contact, Organisation_contact,
                   Position_contact, Tel_contact, DeliveryPoint, CodePostal, Ville, Pays, Email, SystemReference,
                   westBoundLongitude, EastBoundLongitude, SouthBoundLatitude, NorthBoundLatitude, Titre,
                   FicheParent, Abstract, Date_creation, Purpose, Status, Freq_maj, liste_dates, SupplementInfo,
                   UseLimitation, UseContrainte, AccesContrainte, AutreContrainte,
                   Format, Online_links, Online_protocols, Online_description, Online_nom,
                   Niveau, Conformite, Genealogie, Scope, groupe, mention, Thesaurus, Themes, Keywords, 
                   F1, F2, F3, F4, A1, A2, I1, I2, I3, R1, R2, R3]


liste_columns_df = ['Identifiant', 'Langue', 'Jeu de caractères', 'Type', 'Date', 'Nom du standard', 'Version du standard', 'Nom du contact', 'orga du contact',
                    'Position du contact', 'Tel du contact', 'Adresse', 'Code Postal', 'Ville', 'Pays', 'Email du contact', "Systeme de référence",
                    'Longitude ouest', 'Longitude est', 'Latitude sud', 'Latitude nord', 'Titre',
                    'Fiche parent id', 'Résumé', "Date de création", 'Objectif', 'Status', 'Fréquence de maj', 'Autres dates', 'Info supplémentaire',
                    'Limite usage', 'Contrainte usage', 'Contrainte accès', 'Autre contrainte',
                    'Format', 'Url', 'Protocole', 'Online description', 'Online nom',
                    'Niveau', 'Conformité', 'Généalogie', 'Portée', 'Groupe associé','Mention', 'Thesaurus', 'Thèmes', 'Mots Clés',
                    'F1', 'F2', 'F3', 'F4', 'A1', 'A2', 'I1', 'I2', 'I3', 'R1', 'R2', 'R3']


df_variables_evaluation = pd.DataFrame(data=[liste_variables],columns=liste_columns_df)

##################################################################################################
######### VISUALISATION DE LA FICHE ###############################################################
if 'Recherche' not in st.session_state:
    st.session_state.Recherche = False
if 'Visu_attachments' not in st.session_state:
    st.session_state.Visu_attachments = False
if 'Ressources_associees' not in st.session_state:
    st.session_state.Ressources_associees = False

# Function to handle checkbox1 change
def handle_button1_change():
    if st.session_state.Recherche:
        st.session_state.Visu_attachments = False
        st.session_state.Ressources_associees = False


def handle_button2_change():
    if st.session_state.Visu_attachments:
        st.session_state.Recherche = False
        st.session_state.Ressources_associees = False

# Function to handle checkbox2 change
def handle_button3_change():
    if st.session_state.Ressources_associees:
        st.session_state.Recherche = False
        st.session_state.Visu_attachments = False

def handle_button4_change():
    if st.session_state.copie_id:
        st.session_state.Recherche = False

col1,col2,col3 = st.columns(3)
with col1:
    Recherche = st.checkbox(label='Faire une recherche spécifique', key='Recherche',on_change=handle_button1_change)
with col2:
    Visu_attachments = st.checkbox(label='Fichiers attachés', key='Visu_attachments',on_change=handle_button2_change)
with col3:
    Ressources_associees = st.checkbox(label='Ressources associées', key='Ressources_associees',on_change=handle_button3_change)


if Recherche:
    #st.dataframe(tableau)
    titres = set(tableau['Titre'])
    col1,col2,col3 = st.columns([0.3,0.4,0.3])
    with col1:
        titre_choisi = st.multiselect(label='Trouver un titre',options=titres)
    with col2:
        if len(titre_choisi)!=0:
            id_choisie = tableau['Identifiant'][tableau['Titre']==titre_choisi[0]].values[0]
            st.markdown('')
            st.code(id_choisie)
        else:
            st.metric(label='id',value='')
    with col3:
        if len(titre_choisi)!=0:
            st.markdown('')
            st.markdown("")
            st.markdown("<-- copier l'identifieur")

elif Visu_attachments:
    st.write('en cours de fabrication')
elif Ressources_associees:
    st.write('en cours de fabrication')
else:
    with st.container(border=True):
        s2 = "METADONNEES"
        s_s2 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s2}</p>"
        st.markdown(s_s2,unsafe_allow_html=True)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s2a = 'Date'
            s_s2a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2a}</p>"
            st.markdown(s_s2a,unsafe_allow_html=True)
            st.markdown(Date)
        with col2:
            s2b = 'Langue'
            s_s2b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2b}</p>"
            st.markdown(s_s2b,unsafe_allow_html=True)
            if 'zaaj_' in identifieur:
                for i in range(len(Langue)):
                    st.markdown(Langue[i])
            else:
                st.markdown(Langue)
        with col3:
            s2c = 'Jeu de caractères'
            s_s2c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2c}</p>"
            st.markdown(s_s2c,unsafe_allow_html=True)
            st.markdown(JeuDeCaracteres)
        with col4:
            s2d = 'Type'
            s_s2d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2d}</p>"
            st.markdown(s_s2d,unsafe_allow_html=True)
            st.markdown(Type)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s2e = 'Nom du contact'
            s_s2e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2e}</p>"
            st.markdown(s_s2e,unsafe_allow_html=True)
            for x in range(len(Nom_contact)):
                st.markdown(Nom_contact[x])
        with col2:
            s2f = 'Position du contact'
            s_s2f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2f}</p>"
            st.markdown(s_s2f,unsafe_allow_html=True)
            for x in range(len(Position_contact)):
                st.markdown(Position_contact[x])
        with col3:
            s2g = 'Orga du contact'
            s_s2g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2g}</p>"
            st.markdown(s_s2g,unsafe_allow_html=True)
            for x in range(len(Organisation_contact)):
                st.markdown(Organisation_contact[x])
        with col4:
            s2h = 'Tel du contact'
            s_s2h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2h}</p>"
            st.markdown(s_s2h,unsafe_allow_html=True)
            for x in range(len(Tel_contact)):
                st.markdown(Tel_contact[x])

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s2i = 'Adresse'
            s_s2i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2i}</p>"
            st.markdown(s_s2i,unsafe_allow_html=True)
            for x in range(len(DeliveryPoint)):
                st.markdown(DeliveryPoint[x])
        with col2:
            s2j = 'Code Postal'
            s_s2j = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2j}</p>"
            st.markdown(s_s2j,unsafe_allow_html=True)
            for x in range(len(CodePostal)):
                st.markdown(CodePostal[x])
        with col3:
            s2k = 'Ville'
            s_s2k = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2k}</p>"
            st.markdown(s_s2k,unsafe_allow_html=True)
            for x in range(len(Ville)):
                st.markdown(Ville[x])
        with col4:
            s2l = 'Pays'
            s_s2l = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2l}</p>"
            st.markdown(s_s2l,unsafe_allow_html=True)
            for x in range(len(Pays)):
                st.markdown(Pays[x])

        col1,col2,col3 = st.columns([0.25,0.25,0.5])
        with col1:
            s2m = 'Nom du standard'
            s_s2m = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2m}</p>"
            st.markdown(s_s2m,unsafe_allow_html=True)
            st.markdown(Standard)
        with col2:
            s2n = 'Version du standard'
            s_s2n = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2n}</p>"
            st.markdown(s_s2n,unsafe_allow_html=True)
            st.markdown(Version_standard)
        with col3:
            s2o = 'Adresse email du contact'
            s_s2o = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2o}</p>"
            st.markdown(s_s2o,unsafe_allow_html=True)
            st.markdown(Email)

    with st.container(border=True):
        s3 = "SYSTEME DE REFERENCE & LIMITES GEOGRAPHIQUES"
        s_s3 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s3}</p>"
        st.markdown(s_s3,unsafe_allow_html=True)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s3a = 'Systèmes renseignés'
            s_s3a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3a}</p>"
            st.markdown(s_s3a,unsafe_allow_html=True)
            for x in range(len(SystemReference)):
                st.markdown(SystemReference[x])
        with col2:
            pass
        with col3:
            pass
        with col4:
            pass

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s3c = 'Longitude Ouest'
            s_s3c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3c}</p>"
            st.markdown(s_s3c,unsafe_allow_html=True)
            st.markdown(westBoundLongitude)
        with col2:
            s3d = 'Longitude Est'
            s_s3d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3d}</p>"
            st.markdown(s_s3d,unsafe_allow_html=True)
            st.markdown(EastBoundLongitude)
        with col3:
            s3e = 'Latitude Sud'
            s_s3e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3e}</p>"
            st.markdown(s_s3e,unsafe_allow_html=True)
            st.markdown(SouthBoundLatitude)
        with col4:
            s3f = 'Latitude Nord'
            s_s3f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3f}</p>"
            st.markdown(s_s3f,unsafe_allow_html=True)
            st.markdown(NorthBoundLatitude)

    with st.container(border=True):
        s4 = "IDENTIFICATION"
        s_s4 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s4}</p>"
        st.markdown(s_s4,unsafe_allow_html=True)

        col1,col2 = st.columns(2)
        with col1:
            s4a = 'Titre'
            s_s4a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4a}</p>"
            st.markdown(s_s4a,unsafe_allow_html=True)
            st.markdown(Titre)
        with col2:
            s4a_ = 'Fiche Parent'
            s_s4a_ = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4a_}</p>"
            st.markdown(s_s4a_,unsafe_allow_html=True)
            st.markdown(FicheParent)

        s4b = 'Résumé'
        s_s4b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4b}</p>"
        st.markdown(s_s4b,unsafe_allow_html=True)
        if 'zaaj_' in identifieur:
            for i in range(len(Abstract)):
                st.markdown(Abstract[i])
        else:
            st.markdown(Abstract)

        col1,col2,col3 = st.columns(3)
        with col1:
            s4d = 'Purpose'
            s_s4d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4d}</p>"
            st.markdown(s_s4d,unsafe_allow_html=True)
            st.markdown(Purpose)
        with col2:
            s4e = 'Status'
            s_s4e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4e}</p>"
            st.markdown(s_s4e,unsafe_allow_html=True)
            st.markdown(Status)
        with col3:
            s4f = 'Fréquence de maj'
            s_s4f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4f}</p>"
            st.markdown(s_s4f,unsafe_allow_html=True)
            st.markdown(Freq_maj)

        col1,col2,col3 =st.columns(3)
        with col1:
            s4c = 'Date (création)'
            s_s4c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4c}</p>"
            st.markdown(s_s4c,unsafe_allow_html=True)
            st.markdown(Date_creation)
        with col2:
            try:
                s4g = f'Date ({liste_dates[0][0]})'
                s_s4g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4g}</p>"
                st.markdown(s_s4g,unsafe_allow_html=True)
                st.markdown(liste_dates[0][1])
            except:
                pass
        with col3:
            try:
                s4h = f'Date ({liste_dates[1][0]})'
                s_s4h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4h}</p>"
                st.markdown(s_s4h,unsafe_allow_html=True)
                st.markdown(liste_dates[1][1])
            except:
                pass
        
        s4i = f'Info Supplémentaire'
        s_s4i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4i}</p>"
        st.markdown(s_s4i,unsafe_allow_html=True)
        st.markdown(SupplementInfo)

    with st.container(border=True):
        s5 = "MOTS CLES"
        s_s5 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s5}</p>"
        st.markdown(s_s5,unsafe_allow_html=True)

        col1,col2,col3 = st.columns(3)
        with col1:
            s5a = f'Thésaurus éventuel'
            s_s5a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5a}</p>"
            st.markdown(s_s5a,unsafe_allow_html=True)
        with col2:
            s5b = f'Type de mots clés'
            s_s5b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5b}</p>"
            st.markdown(s_s5b,unsafe_allow_html=True)
        with col3:
            s5c = f'Mots Clés'
            s_s5c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5c}</p>"
            st.markdown(s_s5c,unsafe_allow_html=True)

        for j in range(len(theme_thesaurus_motsCles)):
            col1,col2,col3 = st.columns(3)
            with col1:
                st.markdown(theme_thesaurus_motsCles[j][2])
            with col2:
                st.markdown(theme_thesaurus_motsCles[j][1])
            with col3:
                if 'zaaj_' in identifieur:
                    for i in range(len(Mots_cles_zaaj)):
                        st.markdown(Mots_cles_zaaj[i])
                else:
                    for i in range(len(theme_thesaurus_motsCles[j][0])):
                        st.markdown(theme_thesaurus_motsCles[j][0][i])

    with st.container(border=True):
        s6 = "CONTRAINTES"
        s_s6 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s6}</p>"
        st.markdown(s_s6,unsafe_allow_html=True)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s6a = "Limite d'Accès"
            s_s6a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6a}</p>"
            st.markdown(s_s6a,unsafe_allow_html=True)
            st.markdown(AccesContrainte)
        with col2:
            s6b = "Contrainte d'usage"
            s_s6b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6b}</p>"
            st.markdown(s_s6b,unsafe_allow_html=True)
            if 'zaaj_' in identifieur:
                for i in range(len(UseContrainte)):
                    st.markdown(UseContrainte[i])
            else:
                st.markdown(UseContrainte)
        with col3:
            s6c = "Limite d'Usage"
            s_s6c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6c}</p>"
            st.markdown(s_s6c,unsafe_allow_html=True)
            st.markdown(UseLimitation)
        with col4:
            s6d = "Autre contrainte"
            s_s6d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6d}</p>"
            st.markdown(s_s6d,unsafe_allow_html=True)
            st.markdown(AutreContrainte)

    with st.container(border=True):
        s7 = "DISTRIBUTION"
        s_s7 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s7}</p>"
        st.markdown(s_s7,unsafe_allow_html=True)

        col1,col2 = st.columns([0.7,0.3])
        with col1:
            s7b = "URL"
            s_s7b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7b}</p>"
            st.markdown(s_s7b,unsafe_allow_html=True)
            if 'zaaj_' in identifieur:
                for x in range(len(Online_links)):
                        st.markdown(Online_links[x])
            else:
                try:
                    for x in range(len(Online_links)):
                            st.markdown(Online_links[x])
                except:
                    pass
        with col2:
            s7c = "Protocole"
            s_s7c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7c}</p>"
            st.markdown(s_s7c,unsafe_allow_html=True)
            try:
                for x in range(len(Online_protocols)):
                        st.markdown(Online_protocols[x])
            except:
                pass
        
        col1,col2,col3 = st.columns([0.3,0.4,0.3])
        with col1:
            s7d = "Nom de la ressource"
            s_s7d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7d}</p>"
            st.markdown(s_s7d,unsafe_allow_html=True)
            try:
                for x in range(len(Online_nom)):
                        st.markdown(Online_nom[x])
            except:
                pass
        with col2:
            s7e = "Description de la ressource"
            s_s7e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7e}</p>"
            st.markdown(s_s7e,unsafe_allow_html=True)
            try:
                for x in range(len(Online_description)):
                        st.markdown(Online_description[x])
            except:
                pass
        with col3:
            s7a = "Format"
            s_s7a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7a}</p>"
            st.markdown(s_s7a,unsafe_allow_html=True)
            try:
                for x in range(len(Format)):
                        st.markdown(Format[x])
            except:
                pass

    with st.container(border=True):
        s8 = "QUALITE"
        s_s8 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s8}</p>"
        st.markdown(s_s8,unsafe_allow_html=True)

        col1,col2 = st.columns(2)
        with col1:
            s8a = "Niveau"
            s_s8a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8a}</p>"
            st.markdown(s_s8a,unsafe_allow_html=True)
            st.markdown(Niveau)

        with col2:
            s8b = "Conformité"
            s_s8b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8b}</p>"
            st.markdown(s_s8b,unsafe_allow_html=True)
            st.markdown(Conformite)

        col1,col2 = st.columns(2)
        with col1:
            s8c = "Généalogie"
            s_s8c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8c}</p>"
            st.markdown(s_s8c,unsafe_allow_html=True)
            st.markdown(Genealogie)
        with col2:
            s8d = "Portée"
            s_s8d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8d}</p>"
            st.markdown(s_s8d,unsafe_allow_html=True)
            st.markdown(Scope)


##################################################################################################
########## VISUALISATION DU GROUPE ###############################################################

lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'

st.sidebar.markdown('Groupe et Mention')
col1,col2 = st.sidebar.columns(2)
with col1:
    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                            {wch_colour_box[1]}, 
                                                            {wch_colour_box[2]}, 0.75); 
                                        color: rgb({wch_colour_font[0]}, 
                                                {wch_colour_font[1]}, 
                                                {wch_colour_font[2]}, 0.75); 
                                        font-size: {fontsize}px; 
                                        border-radius: 7px; 
                                        padding-left: 12px; 
                                        padding-top: 10px; 
                                        padding-bottom: 10px; 
                                        line-height:5px;
                                        text-align:center'>
                                        </style><BR><span style='font-size: 25px; 
                                        margin-top: 0;'>{groupe}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)
with col2:
    htmlstr2 = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                            {wch_colour_box[1]}, 
                                                            {wch_colour_box[2]}, 0.75); 
                                        color: rgb({wch_colour_font[0]}, 
                                                {wch_colour_font[1]}, 
                                                {wch_colour_font[2]}, 0.75); 
                                        font-size: {fontsize}px; 
                                        border-radius: 7px; 
                                        padding-left: 12px; 
                                        padding-top: 10px; 
                                        padding-bottom: 10px; 
                                        line-height:5px;
                                        text-align:center'>
                                        </style><BR><span style='font-size: 25px; 
                                        margin-top: 0;'>{mention}</style></span></p>"""
    st.markdown(lnk + htmlstr2, unsafe_allow_html=True)

##################################################################################################
####################### VISUALISATION FAIR ####################################################
st.sidebar.markdown('Matrice FAIR')
col0,col1,col2,col3, col4 = st.sidebar.columns([0.1,0.22,0.22,0.22,0.22])
with col0:
    st.markdown("F")
with col1:
    htmlstr = f"""<p style='background-color: rgb({F1c[0]}, 
                                                        {F1c[1]}, 
                                                        {F1c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75);  
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:10px;
                                    text-align:left'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)
with col2:
    htmlstr = f"""<p style='background-color: rgb({F2c[0]}, 
                                                        {F2c[1]}, 
                                                        {F2c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:8px;
                                    text-align:center'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)
with col3:
    htmlstr = f"""<p style='background-color: rgb({F3c[0]}, 
                                                        {F3c[1]}, 
                                                        {F3c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:8px;
                                    text-align:center'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)
with col4:
    htmlstr = f"""<p style='background-color: rgb({F4c[0]}, 
                                                        {F4c[1]}, 
                                                        {F4c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:8px;
                                    text-align:center'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)

col0,col1,col2 = st.sidebar.columns([0.1,0.45,0.45])
with col0:
    st.markdown("A")
with col1:
    htmlstr = f"""<p style='background-color: rgb({A1c[0]}, 
                                                        {A1c[1]}, 
                                                        {A1c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:8px;
                                    text-align:center'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)
with col2:
    htmlstr = f"""<p style='background-color: rgb({A2c[0]}, 
                                                        {A2c[1]}, 
                                                        {A2c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:8px;
                                    text-align:center'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)

col0,col1,col2,col3 = st.sidebar.columns([0.1,0.3,0.3,0.3])
with col0:
    st.markdown("I")
with col1:
    htmlstr = f"""<p style='background-color: rgb({I1c[0]}, 
                                                        {I1c[1]}, 
                                                        {I1c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:8px;
                                    text-align:center'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)
with col2:
    htmlstr = f"""<p style='background-color: rgb({I2c[0]}, 
                                                        {I2c[1]}, 
                                                        {I2c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:8px;
                                    text-align:center'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)
with col3:
    htmlstr = f"""<p style='background-color: rgb({I3c[0]}, 
                                                        {I3c[1]}, 
                                                        {I3c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:8px;
                                    text-align:center'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)

col0,col1,col2,col3 = st.sidebar.columns([0.1,0.3,0.3,0.3])
with col0:
    st.markdown("R")
with col1:
    htmlstr = f"""<p style='background-color: rgb({R1c[0]}, 
                                                        {R1c[1]}, 
                                                        {R1c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:8px;
                                    text-align:center'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)
with col2:
    htmlstr = f"""<p style='background-color: rgb({R2c[0]}, 
                                                        {R2c[1]}, 
                                                        {R2c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:8px;
                                    text-align:center'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)
with col3:
    htmlstr = f"""<p style='background-color: rgb({R3c[0]}, 
                                                        {R3c[1]}, 
                                                        {R3c[2]}, 0.75); 
                                    color: rgb({wch_colour_font[0]}, 
                                            {wch_colour_font[1]}, 
                                            {wch_colour_font[2]}, 0.75); 
                                    font-size: 10px; 
                                    border-radius: 7px; 
                                    padding-left: 5px; 
                                    padding-top: 5px; 
                                    padding-bottom: 5px; 
                                    line-height:8px;
                                    text-align:left'>
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{""}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)

###############################################################################################
########### POUR L'ADMINISTRATEUR ############################################################
###############################################################################################

# Mot de passe pour faire des récupérations automatisées
admin_pass = 'admin'
admin_action = st.sidebar.text_input(label="Pour l'administrateur")


# RECUPERATION DES IDENTIFIANTS VIA BOUTON ##########################################

if admin_action == admin_pass:

        RecupIdentifiants = st.sidebar.button("Récupération des identifiants")
        if RecupIdentifiants:
            with st.spinner("Connexion au GeoNetwork et récupération des identifiants existants"):
                scraping_GN(d)   
                uuids_cleaning(d)
                st.experimental_rerun()

# RECUPERATION DES GROUPES VIA BOUTON ###############################################

if admin_action == admin_pass:
    Recup_groupes = st.sidebar.button('recup des groupes')
    if Recup_groupes:
        with st.spinner("La récup des groupes est en cours"):
            groupes = []
            liste_u = []
            for i in range(len(uuids)):
                u = uuids.loc[i,'uuid_cat_InDoRes']
                try:
                    g = recup_group(uuid=u)
                    groupes.append(g)
                    liste_u.append(u)
                except:
                    g = ""
                    groupes.append(g)
                    liste_u.append(u)

            df_group = pd.DataFrame({'Identifiant':liste_u, 'Groupe':groupes})
            df_group.to_csv("pages/data/infos_MD/infos_groupes.csv")

# RECUPERATION GLOBALE ################################################

if admin_action == admin_pass:
    Recup_globale = st.sidebar.button('recup globale')
    if Recup_globale:
        with st.spinner("La récup globale est en cours"):
            liste_columns_df = ['Identifiant','Langue','Date','Standard','Version_standard','Nom_contact','Orga_contact',
                                'Position_contact','Longitude_Ouest','Longitude_Est','Latitude_Sud','Latitude_Nord','Titre',
                                'Thesaurus','Themes','Mots_clés','Limite_usage','Contrainte_usage','Format','URL','F2','A1','I1','I2','R1','R2','Groupe_et_Mention']
            df_global = pd.DataFrame(columns=liste_columns_df)
            for i in range(len(df_infos)):
                print(i)
                identif = df_infos.loc[i,'Identifiant']
                datafri, mention, groupe_et_mention = recup_fiche(url, identif, headers_json, headers_xml, couleur_True, couleur_False, df_infos, filtre_mention)
                df_infos.loc[i,'Mention'] = mention
                df_infos.loc[i,'Groupe_et_Mention'] = groupe_et_mention
                new_df_global = pd.concat([df_global,datafri], axis=0)
                df_global = new_df_global
                df_global.reset_index(inplace=True)
                df_global.drop(columns='index',inplace=True)
            df_global.to_csv("pages/data/infos_MD/Tableau_MD.csv")
            df_infos.to_csv(("pages/data/infos_MD/infos_groupes_mentions.csv"))