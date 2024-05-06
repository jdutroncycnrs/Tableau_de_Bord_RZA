import pandas as pd
import re

data = pd.read_csv("pages\data\Enregistrements_RZA_060524.csv")
data.rename(columns={"createDate":"Date"}, inplace=True)

for i in range(len(data)):
    if data.loc[i,'Org']=='-':
        data.loc[i,'Org']='non renseigné'

for i in range(len(data)):
    try:
        l = data.loc[i,'Org']
        data.loc[i,'Org']=re.split(',',l)[0]
        if data.loc[i,'Org']=='LETG UMR 6554 CNRS':
            data.loc[i,'Org']='UMR6554 LETG CNRS'
        if data.loc[i,'Org']=='Sorbonne Université - Metis':
            data.loc[i,'Org']='UMR 7619 Metis Sorbonne Université'
        if data.loc[i,'Org']=='Sorbonne Université - UMR 7619 Metis':
            data.loc[i,'Org']='UMR 7619 Metis Sorbonne Université'
        if data.loc[i,'Org']=='CNRS - ECCOREV (FR3098)':
            data.loc[i,'Org']='ECCOREV (FR3098) - CNRS'
        if data.loc[i,'Org']=='CNRS - ECCOREV (FR3098) - OHM Bassin minier de Provence':
            data.loc[i,'Org']='ECCOREV (FR3098) - CNRS'
        if data.loc[i,'Org']=='LETG-Rennes Costel':
            data.loc[i,'Org']='UMR6554 LETG CNRS'
        if data.loc[i,'Org']=='LETG-RENNES UMR 6554 CNRS Université de Rennes 2' :
            data.loc[i,'Org']='UMR6554 LETG CNRS'            
    except:
        pass

data_orga = data['Org']
cnt = data_orga.value_counts()[0:30]
print(cnt)