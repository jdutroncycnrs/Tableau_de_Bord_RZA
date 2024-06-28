import streamlit as st
import pandas as pd
import requests
import json
import os.path
from os import path
import re
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
import glob
import time

from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Analyse des Dataverses",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

##########################  VARIABLES DE CONNEXION #######################
BASE_URL="https://data.indores.fr"
API_TOKEN="19f0769d-564f-44ac-809b-22853f186960"
##########################################################################

###################### CREATION CONNEXION ##############################
with st.spinner("Connexion au Dataverse Data.InDoRes en cours"):
    api = NativeApi(BASE_URL, API_TOKEN)
    resp = api.get_info_version()
    response = resp.json()

col1, col2 = st.columns(2)
with col1:
    d = datetime.date.today()
    if response['status']=='OK':
        st.write(f"La connexion est établie avec Data.InDoRes")
    else: 
        st.write(f"La connexion a échoué, vous n'êtes pas connecté à Data.InDoRes")

with col2:
    b1 = st.button(label=" Mise à jour des entrepôts Dataverses dans Data.InDoRes ")

fichier = f'tableau_dataverses-{d}.csv'
fi = glob.glob(f"pages/data/tableau_dataverses*.csv")

if len(fi)!=0:
    fich = fi[-1]
    data = pd.read_csv(fich)
    fig = px.sunburst(data, path=['niv0','niv1', 'niv2','niv3'], values='val')
    fig.update_layout(
        title=f'Visuel des différents Dataverses dans Data.InDoRes via {fich}',
        width=1000,
        height=1000)
    st.plotly_chart(fig,use_container_width=True)
else:
     st.write('Il est nécessaire de mettre à jour vos entrepôts')

if b1==True:
    with st.spinner("Récupération des entrepôts existants"):
        # On peut aller chercher le contenu du dataverse
        # le status est rappelé puis on a une clé "data" dans laquelle on retrouve son contenu.
        # Pour dataindores: d'autres sous-dataverses!
        dataindores = api.get_dataverse_contents("dataindores")
        data_indores = dataindores.json()
        # Ici on récupère les noms de ces dataverses et les id 
        # On crée un premier tableau avec ces élements
        liste_dataverses_1= []
        liste_ids = []
        for d in range(len(data_indores['data'])):
            if data_indores['data'][d]['type']=="dataverse":
                liste_dataverses_1.append(data_indores['data'][d]['title'])
                liste_ids.append(data_indores['data'][d]['id'])
        df_liste_dataverses_1=pd.DataFrame(data=[liste_dataverses_1,liste_ids], index=['Dataverses_niv1','Ids'])
        df_liste_dataverses_1=df_liste_dataverses_1.T
        # A partir de ce tableau, pour chacun des dataverses répertoriés (niv1), on récupère les noms des sous-dataverses (niv2) 
        # On enregistre ces infos dans un csv
        liste = []
        ids = []
        for i in range(len(df_liste_dataverses_1)):
            datav = api.get_dataverse_contents(df_liste_dataverses_1.loc[i,'Ids'])
            datav_dv = datav.json()
            liste_dataverses_2 = []
            ids_niv2 = []
            for d in range(len(datav_dv['data'])):
                try:
                    if datav_dv['data'][d]['type']=="dataverse":
                        liste_dataverses_2.append(datav_dv['data'][d]['title'])
                        ids_niv2.append(datav_dv['data'][d]['id'])
                except:
                        liste_dataverses_2.append()
                        ids_niv2.append()
            liste.append(liste_dataverses_2)
            ids.append(ids_niv2)
            
        df_liste_dataverses_1['Dataverses_niv2']=liste
        df_liste_dataverses_1['Ids_niv2']=ids
        df_liste_dataverses_1.to_csv(f"pages/data/liste_dataverses.csv")
            
        df_liste_dataverses_2=pd.DataFrame(data=[liste,ids], index=['Dataverses_niv2','Ids_niv2'])
        df_liste_dataverses_2=df_liste_dataverses_2.T
        df_liste_dataverses_2.to_csv(f"pages/data/liste_dataverses2.csv")

        data = pd.read_csv(f"pages/data/liste_dataverses.csv")
        data.drop(columns=['Unnamed: 0'], inplace=True)
        for i in range(len(data)):
                data.loc[i,'val']=int(len(re.split(',',data.loc[i,'Dataverses_niv2'].replace('[','').replace(']','').replace("'",'').strip())))

        som = sum(data['val'].values)
        new_data = pd.DataFrame(index=np.arange(0,som), columns=['niv1','niv2'])
        i=0
        for j in range(len(data)):
            for k in range(int(data.loc[j,'val'])):
                new_data.loc[i,'niv1']=data.loc[j,'Dataverses_niv1']
                new_data.loc[i,'ids_niv1']=data.loc[j,'Ids']
                new_data.loc[i,'niv2']=re.split(',',data.loc[j,'Dataverses_niv2'].replace('[','').replace(']','').replace("'",'').strip())[k]
                new_data.loc[i,'ids_niv2']=re.split(',',data.loc[j,'Ids_niv2'].replace('[','').replace(']','').replace("'",'').strip())[k]
                i+=1
        new_data['val']=1
        new_data['niv0']="Data_InDoRes"
        new_data.to_csv(f"pages/data/{fichier}")

        dat = pd.read_csv(f"pages/data/{fichier}")
        dat_ = dat.copy()
        dat_.drop(columns=['Unnamed: 0'], inplace=True)
        dat_.dropna(axis=0,inplace=True)
        dat_['ids_niv2'] = dat_['ids_niv2'].astype(int)
        liste_bis = []
        ids_bis = []
        for i in range(len(dat)):
            liste_dataverses_3 = []
            ids_niv3 = []
            try:
                datav_ = api.get_dataverse_contents(dat_.loc[i,'ids_niv2'])
                datav_dv_ = datav_.json()       
                try:
                    h = len(datav_dv_['data'])
                    for d in range(h):
                        if datav_dv_['data'][d]['type']=="dataverse":
                            liste_dataverses_3.append(datav_dv_['data'][d]['title'])
                            ids_niv3.append(datav_dv_['data'][d]['id'])
                        else:
                            liste_dataverses_3.append('')
                            ids_niv3.append('')
                except:
                    liste_dataverses_3.append('')
                    ids_niv3.append('')
            except:
                liste_dataverses_3.append('')
                ids_niv3.append('')
            liste_bis.append(liste_dataverses_3)
            ids_bis.append(ids_niv3)

        dat['Dataverses_niv3']=liste_bis
        dat['Ids_niv3']=ids_bis

        for i in range(len(dat)):
            try:
                o = dat.loc[i,'Dataverses_niv3'][0]
                p = dat.loc[i,'Ids_niv3'][0]
                dat.loc[i,'niv3']=o
                dat.loc[i,'ids_niv3']=p
            except:
                dat.loc[i,'niv3']=None
                dat.loc[i,'ids_niv3']=None
        dat.drop(columns=['Dataverses_niv3','Ids_niv3'], inplace=True)
        dat.to_csv(f"pages/data/{fichier}")

        ###################################  Visualisation ######################################
        test = pd.read_csv(f"pages/data/{fichier}")
        fig = px.sunburst(test, path=['niv0','niv1', 'niv2','niv3'], values='val')
        fig.update_layout(
            title=f'Visuel des différents Dataverses dans Data.InDoRes via {fichier}',
            width=1000,
            height=1000)
        st.plotly_chart(fig,use_container_width=True)


st.title("Analyse des entrepôts")
liste_ZAs= ['ZAA','ZAAJ','ZAAR','ZAEU','ZABR','ZABRI','ZAM','ZAL','ZAS','ZAPygar','ZATU','ZAPVS','ZAH','ZARG','ZACAM','ZATA']
liste_ZAs_ = [' Zone atelier Alpes',' Zone atelier arc jurassien',' Zone atelier Armorique',' Zone atelier environnementale urbaine',' Zone atelier bassin du Rhône',' Zone atelier Brest Iroise',' Zone atelier bassin de la Moselle',' Zone atelier Loire',' Zone Atelier Seine',' Zone atelier Pyrénées Garonne','Zone atelier territoires uranifères',' Zone atelier Plaine et Val de Sèvre',' Zone atelier Hwange','Zone atelier Environnementale Rurale','Zone atelier Santé Environnement Camargue','Zone atelier Antarctique et terres Australes']
colors = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0','#F9A2BF','#3E9399','#3D4A81','#ECDCC5','#D2CFC8','grey','grey','grey']
colors2 = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0','#F9A2BF','#3E9399','#3D4A81','grey','grey','grey']

all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)


if len(Selection_ZA)!=0:
    with st.container(border=True):
        progress_text = "Operation en cours. Attendez svp."
        my_bar = st.progress(0, text=progress_text)
        liste_contenu = []
        liste_identifiers_dataset = []
        for i in range(len(Selection_ZA)):
            time.sleep(0.01)
            try:
                s = int(data['ids_niv2'][data['niv2']==Selection_ZA[i]].values)
                datav = api.get_dataverse_contents(s)
                datav_contenu = datav.json()
                if datav_contenu["data"][0]['type']!="dataverse":
                    liste_contenu.append(len(datav_contenu["data"]))
                    st.write(datav_contenu["data"])
                else:
                    st.write(datav_contenu["data"])
                    s = datav_contenu["data"][0]['id']
                    datav_bis = api.get_dataverse_contents(s)
                    datav_contenu_bis = datav_bis.json()
                    st.write(datav_contenu_bis["data"])
                    liste_contenu.append(0)
                try:
                    for i in range(len(datav_contenu["data"])):
                        liste_identifiers_dataset.append(datav_contenu["data"][i]['identifier'])
                except:
                    pass
            except:
                liste_contenu.append(0)
            my_bar.progress(i + 1, text=progress_text)
    
        df = pd.DataFrame(liste_contenu,index=liste_ZAs,columns=['Nombre_dépôts'])
        fig0= go.Figure()
        for i, za in enumerate(df.index.values):
            selec = df.index.values[i:i+1]
            selec_len = df['Nombre_dépôts'].values[i:i+1]
            fig0.add_trace(go.Bar(
                        x=selec,
                        y=selec_len,
                        name=za,
                        marker=dict(color=colors2[i])
                    ))
        fig0.update_layout(
                                title='Nombre de dépôts répertoriées au 06/06/24',
                                width=1000,
                                height=500)
        st.plotly_chart(fig0,use_container_width=True)
        my_bar.empty()


        authority = "10.48579"
        st.write(liste_identifiers_dataset)
        
        for identifier in liste_identifiers_dataset:
            dataset = api.get_dataset(identifier=f"doi:{authority}/{identifier}")
            dataset_ = dataset.json()
            st.write(dataset_["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"][0]["value"])