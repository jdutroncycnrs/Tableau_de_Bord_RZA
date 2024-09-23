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
            for i in range(2100):
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

identifieur = uuids.loc[10,'uuid_cat_InDoRes']
# recup du tableau des métadonnées pour une fiche
df = recup_fiche2(url, identifieur, headers_json, filtre_mention)
#st.dataframe(df)

#############################################################################

df_complet = pd.read_csv("pages/data/infos_MD2/Tableau_complet.csv", index_col=[0])
st.dataframe(df_complet)

##################################################################################################
######################## VISUALISATIONS ############################################################
##################################################################################################

