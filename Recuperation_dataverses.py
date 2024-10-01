import pandas as pd
import numpy as np
import re
from pyDataverse.models import Dataset, Dataverse
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi
import json
import requests
import streamlit as st

def Recup_contenu_dataverse(api,s):
    datav = api.get_dataverse_contents(s)
    datav_contenu = datav.json()
    return datav_contenu

def Recup_contenu_dataset(api,persistenteUrl):
    dataset = api.get_dataset(persistenteUrl)
    dataset_contenu = dataset.json()
    return dataset_contenu

def Recup_contenu(api,s, entrepot):
    identifieurs = []
    persistentUrls = []
    datesPublication = []
    selections = []
    entrepot_selected = []
    titre = []
    auteur = []
    auteur_affiliation = []
    auteur_email = []
    resume = []
    subject = []
    publication_url = []
    try:
        datav_contenu = Recup_contenu_dataverse(api,s)
        if len(datav_contenu['data'])==0:
            pass
        else:
            for j in range(len(datav_contenu['data'])):
                test_type = datav_contenu["data"][j]['type']
                if test_type =="dataverse":
                    s2 = datav_contenu["data"][j]['id']
                    sousdatav_contenu = Recup_contenu_dataverse(api,s2)
                    for k in range(len(sousdatav_contenu['data'])):
                        try:
                            identifieur = sousdatav_contenu["data"][k]['identifier']
                            identifieurs.append(identifieur)
                        except:
                            identifieurs.append("")
                        try: 
                            publicationDate = sousdatav_contenu["data"][k]['publicationDate']
                            datesPublication.append(publicationDate)
                        except:
                            datesPublication.append("")
                        try: 
                            persistentUrl = sousdatav_contenu["data"][k]['persistentUrl'].replace('https://doi.org/','doi:')
                            persistentUrls.append(persistentUrl)
                            try:
                                contenu = api.get_dataset_versions(persistentUrl)
                                contenu_json = contenu.json()
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['typeName']=='title':
                                        titre.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['value'])
                                    else:
                                        titre.append('')
                                except:
                                    titre.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                        auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactName']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                        auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactName']['value'])
                                    else:
                                        auteur.append('')
                                except:
                                    auteur.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                        auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactAffiliation']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                        auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactAffiliation']['value'])
                                    else:
                                        auteur_affiliation.append('')
                                except:
                                    auteur_affiliation.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                        auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactEmail']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                        auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactEmail']['value'])
                                    else:
                                        auteur_email.append('')
                                except:
                                    auteur_email.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='dsDescription':
                                        resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['dsDescriptionValue']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='dsDescription':
                                        resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0]['dsDescriptionValue']['value'])
                                    else:
                                        resume.append('')
                                except:
                                    resume.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='subject':
                                        subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['typeName']=='subject':
                                        subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['value'][0])
                                    else:
                                        subject.append('')
                                except:
                                    subject.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['typeName']=='publication':
                                        publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['value'][0]['publicationURL']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['typeName']=='publication':
                                        publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['value'][0]['publicationURL']['value'])
                                    else:
                                        publication_url.append('')
                                except:
                                    publication_url.append('')
                            except:
                                titre.append("")
                                auteur.append('')
                                auteur_affiliation.append('')
                                auteur_email.append('')
                                resume.append('')
                                subject.append('')
                                publication_url.append('')
                        except:
                            persistentUrls.append("")
                            titre.append("")
                            auteur.append('')
                            auteur_affiliation.append('')
                            auteur_email.append('')
                            resume.append('')
                            subject.append('')
                            publication_url.append('')
                        selections.append(s)
                        entrepot_selected.append(entrepot)
                        
                elif test_type == "dataset":
                    try:
                        identifieur = datav_contenu["data"][j]['identifier']
                        identifieurs.append(identifieur)
                    except:
                        identifieurs.append("")
                    try: 
                        publicationDate = datav_contenu["data"][j]['publicationDate']
                        datesPublication.append(publicationDate)
                    except:
                        datesPublication.append("")
                    try: 
                        persistentUrl = datav_contenu["data"][j]['persistentUrl'].replace('https://doi.org/','doi:')
                        persistentUrls.append(persistentUrl)
                        try:
                            contenu = api.get_dataset_versions(persistentUrl)
                            contenu_json = contenu.json()
                            #st.write(contenu_json)
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['typeName']=='title':
                                    titre.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['value'])
                                else:
                                    titre.append('')
                            except:
                                titre.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                    auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactName']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                    auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactName']['value'])
                                else:
                                    auteur.append('')
                            except:
                                auteur.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                    auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactAffiliation']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                    auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactAffiliation']['value'])
                                else:
                                    auteur_affiliation.append('')
                            except:
                                    auteur_affiliation.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                    auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactEmail']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                    auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactEmail']['value'])
                                else:
                                    auteur_email.append('')
                            except:
                                auteur_email.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='dsDescription':
                                   resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['dsDescriptionValue']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='dsDescription':
                                    resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0]['dsDescriptionValue']['value'])
                                else:
                                    resume.append('')
                            except:
                                resume.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='subject':
                                    subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['typeName']=='subject':
                                    subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['value'][0])
                                else:
                                    subject.append('')
                            except:
                                subject.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['typeName']=='publication':
                                    publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['value'][0]['publicationURL']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['typeName']=='publication':
                                    publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['value'][0]['publicationURL']['value'])
                                else:
                                    publication_url.append('')
                            except:
                                publication_url.append('')
                        except:
                            titre.append("")
                            auteur.append('')
                            auteur_affiliation.append('')
                            auteur_email.append('')
                            resume.append('')
                            subject.append('')
                            publication_url.append('')
                    except:
                        persistentUrls.append("")
                        titre.append("")
                        auteur.append('')
                        auteur_affiliation.append('')
                        auteur_email.append('')
                        resume.append('')
                        subject.append('')
                        publication_url.append('')
                    selections.append(s)
                    entrepot_selected.append(entrepot)
    except:
        pass
    df_entrepot = pd.DataFrame({'selection':selections, 
                                'Entrepot':entrepot_selected,
                                'ID':identifieurs,
                                'Url':persistentUrls,
                                'Date de publication':datesPublication,
                                'Titre':titre,
                                'Auteur':auteur,
                                'Organisation':auteur_affiliation,
                                "Email":auteur_email,
                                'Résumé':resume,
                                'Thème':subject,
                                'Publication URL':publication_url
                                })
    return df_entrepot


def Recup_dataverses_rdg(api, fichier):
    RDG = api.get_dataverse_contents("root")
    RDG_json = RDG.json()
    liste_dataverses_1= []
    liste_ids = []
    for d in range(len(RDG_json['data'])):
        if RDG_json['data'][d]['type']=="dataverse":
            liste_dataverses_1.append(RDG_json['data'][d]['title'])
            liste_ids.append(RDG_json['data'][d]['id'])

    df_liste_dataverses_1=pd.DataFrame(data=[liste_dataverses_1,liste_ids], index=['Dataverses_niv1','Ids'])
    df_liste_dataverses_1=df_liste_dataverses_1.T
    
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
    df_liste_dataverses_1.to_csv(f"pages/data/rechercheDataGouv/liste_dataverses_rdg.csv")
            
    df_liste_dataverses_2=pd.DataFrame(data=[liste,ids], index=['Dataverses_niv2','Ids_niv2'])
    df_liste_dataverses_2=df_liste_dataverses_2.T
    df_liste_dataverses_2.to_csv(f"pages/data/rechercheDataGouv/liste_dataverses_rdg2.csv")

    data = pd.read_csv(f"pages/data/rechercheDataGouv/liste_dataverses_rdg.csv")
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
            new_data.loc[i,'niv2']=re.split(',',data.loc[j,'Dataverses_niv2'].replace('[','').replace(']','').strip())[k]
            new_data.loc[i,'niv2']=new_data.loc[i,'niv2'].replace("'","")
            try:
                new_data.loc[i,'ids_niv2']=re.split(',',data.loc[j,'Ids_niv2'].replace('[','').replace(']','').replace('"','').strip())[k]
            except:
                pass
            i+=1
            print(i)
    new_data['val']=1
    new_data['niv0']="Recherche Data Gouv"
    new_data.to_csv(f"pages/data/rechercheDataGouv/{fichier}")


def Recup_dataverses(api, fichier):
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
                new_data.loc[i,'niv2']=re.split(',',data.loc[j,'Dataverses_niv2'].replace('[','').replace(']','').strip())[k]
                new_data.loc[i,'niv2']=new_data.loc[i,'niv2'].replace("'","")
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

def recuperation_zenodo(url_zenodo,params_zenodo, headers_zenodo, ZA):
    
    liste_vide = []
    r = requests.get(url_zenodo,
                    params=params_zenodo,
                    headers=headers_zenodo)
    
    if r.status_code==200:
        resp_zenodo = r.json()['hits']['hits']
        ids = []
        titles = []
        for i in range(len(resp_zenodo)):
            ids.append(resp_zenodo[i]['id'])
            titles.append(resp_zenodo[i]['metadata']['title'])
        reponse_df = pd.DataFrame({'ZA':ZA,
                                   'Ids':ids,
                                   'Titre':titles})
        return reponse_df
    else:
         return liste_vide
    
def recuperation_nakala(url_nakala,params_nakala, headers_nakala, ZA):
    
    liste_vide = []
    r = requests.get(url_nakala,
                    params=params_nakala,
                    headers=headers_nakala)
    
    return r.json()['datas']


## SEANOE 
"""from sickle import Sickle

# SEANOE's OAI-PMH endpoint URL
oai_url = "https://www.seanoe.org/oai/OAIHandler"

# Initialize Sickle with the SEANOE OAI-PMH endpoint
sickle = Sickle(oai_url)

# Example request: List metadata formats
def list_metadata_formats():
    formats = sickle.ListMetadataFormats()
    for metadata_format in formats:
        print(metadata_format)

# Example request: List records
def list_records(metadata_prefix='oai_dc', from_date=None, until_date=None):
    records = sickle.ListRecords(metadataPrefix=metadata_prefix, from_=from_date, until=until_date)
    for record in records:
        print(record.metadata)

# Example request: Get record by ID
def get_record(identifier, metadata_prefix='oai_dc'):
    record = sickle.GetRecord(identifier=identifier, metadataPrefix=metadata_prefix)
    print(record.metadata)

# Run an example function
list_metadata_formats()

# Optionally, list records between dates or get a specific record
# list_records(from_date="2022-01-01", until_date="2022-12-31")
get_record(90452)  # Replace with actual identifier   """

## RDG
"""BASE_URL="https://entrepot.recherche.data.gouv.fr/"
API_TOKEN="b02fd46a-2fb0-4ac3-8717-ae70ec35185a"
api = NativeApi(BASE_URL, API_TOKEN)

datav = api.get_dataverse_contents(142915)
datav_contenu = datav.json()

for i in range(len(datav_contenu)):
    if datav_contenu['data'][i]['type']=='dataverse':
        print(datav_contenu['data'][i])
    elif datav_contenu['data'][i]['type']=='dataset':
        print(datav_contenu['data'][i])
metadata = api.get_dataset(datav_contenu['data'][i]['persistentUrl'])
metadata_json = metadata.json()
data = metadata_json['data']['latestVersion']['metadataBlocks']
print(json.dumps(data, indent=4))"""


## DRYAD
def recuperation_dryad(url_dryad,params_dryad):
    
    liste_vide = []
    r = requests.get(url_dryad,
                    params=params_dryad)
    
    return r.json()

## GBIF
def recuperation_gbif(url_gbif,params_gbif, headers_gbif):
    
    liste_vide = []
    r = requests.get(url_gbif,
                    params=params_gbif,
                    headers=headers_gbif)
    
    return r.json()