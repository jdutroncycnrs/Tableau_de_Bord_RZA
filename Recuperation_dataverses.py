import pandas as pd
import numpy as np
import re
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi

def Recup_contenu_dataverse(api,s):
    datav = api.get_dataverse_contents(s)
    datav_contenu = datav.json()
    return datav_contenu

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
            new_data.loc[i,'niv2']=data.loc[j,'Dataverses_niv2']
            new_data.loc[i,'ids_niv2']=data.loc[j,'Ids_niv2']
            i+=1
            print(i)
    new_data['val']=1
    new_data['niv0']="Recherche Data Gouv"
    new_data.to_csv(f"pages/data/rechercheDataGouv/{fichier}")

    """dat = pd.read_csv(f"pages/data/rechercheDataGouv/{fichier}")
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
    dat.to_csv(f"pages/data/rechercheDataGouv/{fichier}")"""


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