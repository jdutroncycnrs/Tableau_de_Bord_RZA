import streamlit as st
import pandas as pd
import datetime
import glob
import requests
import json
import re
from Recuperation_uuids import scraping_GN, uuids_cleaning
from Traitement_records import transcript_json

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Analyse des fiches de métadonnées du GeoNetwork",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

############ PARAMETRES ############################################

d = datetime.date.today()

url = "https://cat.indores.fr/geonetwork/srv/api/records/"

headers_json = {"accept":"application/json",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}

headers_xml = {"accept":"application/xml",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}

couleur_subtitles = (250,100,0)

############## RECUPERATION DES IDENTIFIANTS EXISTANTS #########################

fi = glob.glob(f"pages/data/uuids/uuid_cat_InDoRes_clean*.csv")

if len(fi)!=0:
    fichier_uuids = fi[-1]
    derniere_date_recup = f"Dernière date de récupération des identifiants: {fichier_uuids[40:-4]}"
    s_derniere_date_recup  = f"<p style='font-size:25px;color:rgb(0,150,0)'>{derniere_date_recup}</p>"
    st.markdown(s_derniere_date_recup ,unsafe_allow_html=True)
    uuids = pd.read_csv(fichier_uuids, index_col=[0])
else:
    st.write('Il est nécessaire de mettre à jour la récupération des uuids')

########### RECUPERATION DES IDENTIFIANTS VIA BOUTON ############################

RecupIdentifiants = st.sidebar.button("Récupération des identifiants")
if RecupIdentifiants:
    with st.spinner("Connexion au GeoNetwork et récupération des identifiants existants"):
        m = scraping_GN(d)   
        uuids_cleaning(d)

########## TITRE DE LA PAGE ############################################
title = "Visualisation des fiches GN"
s_title = f"<p style='font-size:50px;color:rgb(140,140,140)'>{title}</p>"
st.markdown(s_title,unsafe_allow_html=True)

if 'count' not in st.session_state:
    st.session_state.count = 0
def increment_counter():
    st.session_state.count += 1
def reset_counter():
    st.session_state.count = 0

with st.container(border=True):
    sub_title1 = "IDENTIFIEUR"
    s_sub_title1 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title1}</p>"
    st.markdown(s_sub_title1,unsafe_allow_html=True)

    col01,col02,col03 = st.columns([0.8,0.1,0.1])
    with col01:
        identifieur = st.selectbox(label='',options=uuids['uuid_cat_InDoRes'], index=st.session_state.count)
    with col02:
        st.markdown('')
        st.markdown('')
        button1 = st.button(':heavy_plus_sign:',on_click=increment_counter)
    with col03:
        st.markdown('')
        st.markdown('')
        button2 =st.button('R',on_click=reset_counter)

    try:
        df = pd.read_csv(f'pages/data/{identifieur}.csv',index_col=[0])
    except:
        url_ = url + identifieur
        resp1 = requests.get(url_,headers=headers_json)
        if resp1.status_code == 200:
            resp_json=resp1.json()
            with open(f"pages/data/fiches_json/{identifieur}.json", "w") as f:
                json.dump(resp_json, f, indent=4)
            
        resp2 = requests.get(url_,headers=headers_xml)
        if resp2.status_code == 200:
            xml_content = resp2.text
            with open(f"pages/data/fiches_xml/{identifieur}.xml", 'w') as file:
                file.write(xml_content)

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
    st.dataframe(visu, use_container_width=True)