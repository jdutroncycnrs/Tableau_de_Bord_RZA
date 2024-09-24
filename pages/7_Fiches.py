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
from Recuperation_uuids import scraping_GN, uuids_cleaning, recup_group, uuids_cleaning2
from Traitement_records import transcript_json, recup_fiche, recup_fiche2
import ast

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

# Paramètres visuels
couleur_subtitles = (250,150,150)
taille_subtitles = "25px"
couleur_subsubtitles = (60,150,160)
taille_subsubtitles = "25px"

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

################### CREATION / LECTURE DF INFOS GROUPES ##########################################

try:
    df_infos = pd.read_csv("pages/data/infos_MD2/infos_groupes.csv",index_col=[0])
except:
    df_infos = pd.DataFrame(columns=['Identifiant','Groupe'])
    df_infos.to_csv("pages/data/infos_MD2/infos_groupes.csv")

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
            uuids_cleaning2(d)
            st.experimental_rerun()

# RECUPERATION DES GROUPES VIA BOUTON ###############################################

    Recup_groupes = st.sidebar.button('recup des groupes')
    if Recup_groupes:
        with st.spinner("La récup des groupes est en cours"):
            df_group = pd.read_csv("pages/data/infos_MD2/infos_groupes.csv",index_col=[0])
            for i in range(len(uuids)):
                u = uuids.loc[i,'uuid_cat_InDoRes']
                if u in df_group['Identifiant'].values:
                    pass
                else:
                    try:
                        g = recup_group(uuid=u)
                    except:
                        g = ""

                    df_group_i = pd.DataFrame({'Identifiant':[u], 'Groupe':[g]})
                    df_group_ = pd.concat([df_group,df_group_i],axis=0)
                    df_group_.reset_index(inplace=True)
                    df_group_.drop(columns='index',inplace=True)
                    df_group = df_group_
            df_group.to_csv("pages/data/infos_MD2/infos_groupes.csv")

##############################################################################
############## RECUP GLOBALE ###############################################

    Recup_globale = st.sidebar.button('recup globale')
    if Recup_globale:
        with st.spinner("La récup globale est en cours"):
            liste_columns_df = ['Identifiant', 'Langue', 'Jeu de caractères', 'Type', 'Date', 'Nom du standard', 'Version du standard', 'Nom du contact', 'orga du contact',
                            'Position du contact', 'Tel du contact', 'Adresse', 'Code Postal', 'Ville', 'Pays', 'Email du contact', "Systeme de référence",
                            'Longitude ouest', 'Longitude est', 'Latitude sud', 'Latitude nord', 'Titre',
                            'Fiche parent id', 'Résumé', "Date de création", 'Objectif', 'Status', 'Fréquence de maj', 'Autres dates', 'Info supplémentaire',
                            'Limite usage', 'Contrainte usage', 'Contrainte accès', 'Autre contrainte',
                            'Format', 'Url', 'Protocole', 'Online description', 'Online nom',
                            'Niveau', 'Conformité', 'Généalogie', 'Portée','Mention du groupe', 'Thesaurus', 'Thèmes', 'Mots Clés']
            df_global = pd.DataFrame(columns=liste_columns_df)
            for i in range(len(df_infos)):
                print(i)
                identif = df_infos.loc[i,'Identifiant']
                try:
                    datafri = recup_fiche2(url, identif, headers_json, filtre_mention)
                    #df_infos.loc[i,'Mention'] = mention
                    #df_infos.loc[i,'Groupe_et_Mention'] = groupe_et_mention
                    new_df_global = pd.concat([df_global,datafri], axis=0)
                    df_global = new_df_global
                    df_global.reset_index(inplace=True)
                    df_global.drop(columns='index',inplace=True)
                except:
                    pass
            df_global.to_csv("pages/data/infos_MD2/Tableau_MD2.csv")
            #df_infos.to_csv(("pages/data/infos_MD/infos_groupes_mentions.csv"))

            ############## FUSION DES 2 DF: groupes et variables ##########################""
            df_all = pd.merge(df_global, df_infos, on='Identifiant', how='inner')
            df_all.to_csv("pages/data/infos_MD2/Tableau_complet.csv")


##################################################################################################
########## CONNEXION AU GEONETWORK ###############################################################
##################################################################################################

#identifieur = uuids.loc[10,'uuid_cat_InDoRes']
# recup du tableau des métadonnées pour une fiche
#df = recup_fiche2(url, identifieur, headers_json, filtre_mention)
#st.dataframe(df)

#############################################################################

df_complet = pd.read_csv("pages/data/infos_MD2/Tableau_complet.csv", index_col=[0])
df_complet.fillna("", inplace=True)

#def transfo(column):
#    return column.apply(ast.literal_eval)

#df_complet = transfo('Autres dates')
st.dataframe(df_complet)

selected_uuids = df_complet['Identifiant'].values

##################################################################################################
######################## VISUALISATIONS ############################################################
##################################################################################################
if 'count' not in st.session_state:
    st.session_state.count = 0
def increment_counter():
    st.session_state.count += 1
def reset_counter():
    st.session_state.count = 0

if 'Visu_attachments' not in st.session_state:
    st.session_state.Visu_attachments = False
if 'Ressources_associees' not in st.session_state:
    st.session_state.Ressources_associees = False

def handle_button1_change():
    if st.session_state.Visu_attachments:
        st.session_state.Ressources_associees = False

def handle_button2_change():
    if st.session_state.Ressources_associees:
        st.session_state.Visu_attachments = False

with st.container(border=True):
    s1 = "IDENTIFIEUR"
    s_s1 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s1}</p>"
    st.markdown(s_s1,unsafe_allow_html=True)

    if st.session_state.count > len(selected_uuids):
        st.session_state.count = 0

    id_choisie = selected_uuids[0]
    col01,col02,col03,col4,col5 = st.columns([0.5,0.1,0.1,0.1,0.2])
    with col01:
        try:
            identifieur = st.selectbox(label='',options=selected_uuids, index=st.session_state.count)
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
    with col5:
        Visu_attachments = st.checkbox(label='Fichiers attachés', key='Visu_attachments',on_change=handle_button1_change)
        Ressources_associees = st.checkbox(label='Ressources associées', key='Ressources_associees',on_change=handle_button2_change)

    if st.session_state.count > len(selected_uuids):
        st.write('Vous êtes au bout!')


if Visu_attachments:
    st.write('en cours de fabrication')
elif Ressources_associees:
    st.write('en cours de fabrication')
else:
    with st.container(border=True):
        s4 = "IDENTIFICATION"
        s_s4 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s4}</p>"
        st.markdown(s_s4,unsafe_allow_html=True)

        col1,col2 = st.columns(2)
        with col1:
            s4a = 'Titre'
            s_s4a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4a}</p>"
            st.markdown(s_s4a,unsafe_allow_html=True)
            st.markdown(df_complet['Titre'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s4a_ = 'Fiche Parent'
            s_s4a_ = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4a_}</p>"
            st.markdown(s_s4a_,unsafe_allow_html=True)
            st.markdown(df_complet['Fiche parent id'][df_complet['Identifiant']==identifieur].values[0])

        s4b = 'Résumé'
        s_s4b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4b}</p>"
        st.markdown(s_s4b,unsafe_allow_html=True)
        #if 'zaaj_' in identifieur:
            #for i in range(len(Abstract)):
                #st.markdown(Abstract[i])
        #else:
            #st.markdown(Abstract)

        col1,col2,col3 = st.columns(3)
        with col1:
            s4d = 'Purpose'
            s_s4d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4d}</p>"
            st.markdown(s_s4d,unsafe_allow_html=True)
            st.markdown(df_complet['Objectif'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s4e = 'Status'
            s_s4e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4e}</p>"
            st.markdown(s_s4e,unsafe_allow_html=True)
            st.markdown(df_complet['Status'][df_complet['Identifiant']==identifieur].values[0])
        with col3:
            s4f = 'Fréquence de maj'
            s_s4f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4f}</p>"
            st.markdown(s_s4f,unsafe_allow_html=True)
            st.markdown(df_complet['Fréquence de maj'][df_complet['Identifiant']==identifieur].values[0])

        col1,col2,col3 =st.columns(3)
        with col1:
            s4c = 'Date (création)'
            s_s4c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4c}</p>"
            st.markdown(s_s4c,unsafe_allow_html=True)
            st.markdown(df_complet['Date de création'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            #try:
                
                #s4g = f'Date ({df_complet['Autres dates'][df_complet['Identifiant']==identifieur].values[0]})'
                #s_s4g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4g}</p>"
                #st.markdown(s_s4g,unsafe_allow_html=True)
                #st.markdown(df_complet['Autres dates'][df_complet['Identifiant']==identifieur].values[1])
            #except:
                pass
        with col3:
            #try:
                #s4h = f'Date ({liste_dates[1][0]})'
                #s_s4h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4h}</p>"
                #st.markdown(s_s4h,unsafe_allow_html=True)
                #st.markdown(liste_dates[1][1])
            #except:
                pass
        
        s4i = f'Info Supplémentaire'
        s_s4i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4i}</p>"
        st.markdown(s_s4i,unsafe_allow_html=True)
        st.markdown(df_complet['Info supplémentaire'][df_complet['Identifiant']==identifieur].values[0])


    with st.container(border=True):
        s2 = "METADONNEES GENERALES"
        s_s2 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s2}</p>"
        st.markdown(s_s2,unsafe_allow_html=True)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s2a = 'Date'
            s_s2a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2a}</p>"
            st.markdown(s_s2a,unsafe_allow_html=True)
            st.markdown(df_complet['Date'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s2b = 'Langue'
            s_s2b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2b}</p>"
            st.markdown(s_s2b,unsafe_allow_html=True)
            st.markdown(df_complet['Langue'][df_complet['Identifiant']==identifieur].values[0])
        with col3:
            s2c = 'Jeu de caractères'
            s_s2c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2c}</p>"
            st.markdown(s_s2c,unsafe_allow_html=True)
            st.markdown(df_complet['Jeu de caractères'][df_complet['Identifiant']==identifieur].values[0])
        with col4:
            s2d = 'Type'
            s_s2d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2d}</p>"
            st.markdown(s_s2d,unsafe_allow_html=True)
            st.markdown(df_complet['Type'][df_complet['Identifiant']==identifieur].values[0])

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s2e = 'Nom du contact'
            s_s2e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2e}</p>"
            st.markdown(s_s2e,unsafe_allow_html=True)
            #for x in range(len(Nom_contact)):
                #st.markdown(Nom_contact[x])
        with col2:
            s2f = 'Position du contact'
            s_s2f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2f}</p>"
            st.markdown(s_s2f,unsafe_allow_html=True)
            #for x in range(len(Position_contact)):
                #st.markdown(Position_contact[x])
        with col3:
            s2g = 'Orga du contact'
            s_s2g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2g}</p>"
            st.markdown(s_s2g,unsafe_allow_html=True)
            #for x in range(len(Organisation_contact)):
                #st.markdown(Organisation_contact[x])
        with col4:
            s2h = 'Tel du contact'
            s_s2h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2h}</p>"
            st.markdown(s_s2h,unsafe_allow_html=True)
            #for x in range(len(Tel_contact)):
            #    st.markdown(Tel_contact[x])

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s2i = 'Adresse'
            s_s2i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2i}</p>"
            st.markdown(s_s2i,unsafe_allow_html=True)
            #for x in range(len(DeliveryPoint)):
                #st.markdown(DeliveryPoint[x])
        with col2:
            s2j = 'Code Postal'
            s_s2j = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2j}</p>"
            st.markdown(s_s2j,unsafe_allow_html=True)
            #for x in range(len(CodePostal)):
                #st.markdown(CodePostal[x])
        with col3:
            s2k = 'Ville'
            s_s2k = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2k}</p>"
            st.markdown(s_s2k,unsafe_allow_html=True)
            #for x in range(len(Ville)):
                #st.markdown(Ville[x])
        with col4:
            s2l = 'Pays'
            s_s2l = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2l}</p>"
            st.markdown(s_s2l,unsafe_allow_html=True)
            #for x in range(len(Pays)):
                #st.markdown(Pays[x])

        col1,col2,col3 = st.columns([0.25,0.25,0.5])
        with col1:
            s2m = 'Nom du standard'
            s_s2m = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2m}</p>"
            st.markdown(s_s2m,unsafe_allow_html=True)
            st.markdown(df_complet['Nom du standard'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s2n = 'Version du standard'
            s_s2n = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2n}</p>"
            st.markdown(s_s2n,unsafe_allow_html=True)
            st.markdown(df_complet['Version du standard'][df_complet['Identifiant']==identifieur].values[0])
        with col3:
            s2o = 'Adresse email du contact'
            s_s2o = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2o}</p>"
            st.markdown(s_s2o,unsafe_allow_html=True)
            st.markdown(df_complet['Email du contact'][df_complet['Identifiant']==identifieur].values[0])

    with st.container(border=True):
        s3 = "SYSTEME DE REFERENCE & LIMITES GEOGRAPHIQUES"
        s_s3 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s3}</p>"
        st.markdown(s_s3,unsafe_allow_html=True)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s3a = 'Systèmes renseignés'
            s_s3a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3a}</p>"
            st.markdown(s_s3a,unsafe_allow_html=True)
            #for x in range(len(SystemReference)):
                #st.markdown(SystemReference[x])
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
            st.markdown(df_complet['Longitude ouest'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s3d = 'Longitude Est'
            s_s3d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3d}</p>"
            st.markdown(s_s3d,unsafe_allow_html=True)
            st.markdown(df_complet['Longitude est'][df_complet['Identifiant']==identifieur].values[0])
        with col3:
            s3e = 'Latitude Sud'
            s_s3e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3e}</p>"
            st.markdown(s_s3e,unsafe_allow_html=True)
            st.markdown(df_complet['Latitude sud'][df_complet['Identifiant']==identifieur].values[0])
        with col4:
            s3f = 'Latitude Nord'
            s_s3f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3f}</p>"
            st.markdown(s_s3f,unsafe_allow_html=True)
            st.markdown(df_complet['Latitude nord'][df_complet['Identifiant']==identifieur].values[0])

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

        #for j in range(len(theme_thesaurus_motsCles)):
            #col1,col2,col3 = st.columns(3)
            #with col1:
            #    st.markdown(theme_thesaurus_motsCles[j][2])
            #with col2:
            #    st.markdown(theme_thesaurus_motsCles[j][1])
            #with col3:
            #    if 'zaaj_' in identifieur:
            #        for i in range(len(Mots_cles_zaaj)):
            #            st.markdown(Mots_cles_zaaj[i])
            #    else:
            #        for i in range(len(theme_thesaurus_motsCles[j][0])):
            #            st.markdown(theme_thesaurus_motsCles[j][0][i])

    with st.container(border=True):
        s6 = "CONTRAINTES"
        s_s6 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s6}</p>"
        st.markdown(s_s6,unsafe_allow_html=True)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s6a = "Limite d'Accès"
            s_s6a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6a}</p>"
            st.markdown(s_s6a,unsafe_allow_html=True)
            st.markdown(df_complet['Contrainte accès'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s6b = "Contrainte d'usage"
            s_s6b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6b}</p>"
            st.markdown(s_s6b,unsafe_allow_html=True)
            #if 'zaaj_' in identifieur:
            #    for i in range(len(UseContrainte)):
            #        st.markdown(UseContrainte[i])
            #else:
            #    st.markdown(UseContrainte)
        with col3:
            s6c = "Limite d'Usage"
            s_s6c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6c}</p>"
            st.markdown(s_s6c,unsafe_allow_html=True)
            st.markdown(df_complet['Limite usage'][df_complet['Identifiant']==identifieur].values[0])
        with col4:
            s6d = "Autre contrainte"
            s_s6d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6d}</p>"
            st.markdown(s_s6d,unsafe_allow_html=True)
            st.markdown(df_complet['Autre contrainte'][df_complet['Identifiant']==identifieur].values[0])

    with st.container(border=True):
        s7 = "DISTRIBUTION"
        s_s7 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s7}</p>"
        st.markdown(s_s7,unsafe_allow_html=True)

        col1,col2 = st.columns([0.7,0.3])
        with col1:
            s7b = "URL"
            s_s7b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7b}</p>"
            st.markdown(s_s7b,unsafe_allow_html=True)
            #if 'zaaj_' in identifieur:
                #for x in range(len(Online_links)):
                        #st.markdown(Online_links[x])
            #else:
                #try:
                    #for x in range(len(Online_links)):
                    #        st.markdown(Online_links[x])
                #except:
                #    pass
        with col2:
            s7c = "Protocole"
            s_s7c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7c}</p>"
            st.markdown(s_s7c,unsafe_allow_html=True)
            #try:
            #    for x in range(len(Online_protocols)):
            #            st.markdown(Online_protocols[x])
            #except:
            #    pass
        
        col1,col2,col3 = st.columns([0.3,0.4,0.3])
        with col1:
            s7d = "Nom de la ressource"
            s_s7d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7d}</p>"
            st.markdown(s_s7d,unsafe_allow_html=True)
            #try:
            #    for x in range(len(Online_nom)):
            #            st.markdown(Online_nom[x])
            #except:
            #    pass
        with col2:
            s7e = "Description de la ressource"
            s_s7e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7e}</p>"
            st.markdown(s_s7e,unsafe_allow_html=True)
            #try:
            #    for x in range(len(Online_description)):
            #            st.markdown(Online_description[x])
            #except:
            #    pass
        with col3:
            s7a = "Format"
            s_s7a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7a}</p>"
            st.markdown(s_s7a,unsafe_allow_html=True)
            #try:
            #    for x in range(len(Format)):
            #            st.markdown(Format[x])
            #except:
            #    pass

    with st.container(border=True):
        s8 = "QUALITE"
        s_s8 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s8}</p>"
        st.markdown(s_s8,unsafe_allow_html=True)

        col1,col2 = st.columns(2)
        with col1:
            s8a = "Niveau"
            s_s8a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8a}</p>"
            st.markdown(s_s8a,unsafe_allow_html=True)
            st.markdown(df_complet['Niveau'][df_complet['Identifiant']==identifieur].values[0])

        with col2:
            s8b = "Conformité"
            s_s8b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8b}</p>"
            st.markdown(s_s8b,unsafe_allow_html=True)
            st.markdown(df_complet['Conformité'][df_complet['Identifiant']==identifieur].values[0])

        col1,col2 = st.columns(2)
        with col1:
            s8c = "Généalogie"
            s_s8c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8c}</p>"
            st.markdown(s_s8c,unsafe_allow_html=True)
            st.markdown(df_complet['Généalogie'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s8d = "Portée"
            s_s8d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8d}</p>"
            st.markdown(s_s8d,unsafe_allow_html=True)
            st.markdown(df_complet['Portée'][df_complet['Identifiant']==identifieur].values[0])
