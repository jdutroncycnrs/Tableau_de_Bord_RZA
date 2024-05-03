import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
pd.options.mode.chained_assignment = None

##################################### LECTURE DATA ###########################################
data = pd.read_csv("pages/data/Enregistrements_RZA_020524-2.csv")
data.rename(columns={"createDate":"Date"}, inplace=True)

##################################### TRAITEMENT PREALABLE DATES###################################
dico = {'Jan':'01',
        'Feb':'02',
        'Mar':'03',
        'Apr':'04',
        'May':'05',
        'Jun':'06',
        'Jul':'07',
        'Aug':'08',
        'Sep':'09',
        'Oct':'10',
        'Nov':'11',
        'Dec':'12'}
dico2 = {' 1,':' 01',
         ' 2,':' 02',
         ' 3,':' 03',
         ' 4,':' 04',
         ' 5,':' 05',
         ' 6,':' 06',
         ' 7,':' 07',
         ' 8,':' 08',
         ' 4,':' 09'}
for i in range(len(data)):
    for term, num in dico.items():
        data.loc[i,'Date'] = data.loc[i,'Date'].replace(term,num).replace('@','/')
    for term, num in dico2.items():
        data.loc[i,'Date'] = data.loc[i,'Date'].replace(term,num).replace(',','')
    data.loc[i,'Date'] = re.split('/',data.loc[i,'Date'])[0][0:-1].replace(' ','-')+re.split('/',data.loc[i,'Date'])[1]

data['Date'] = pd.to_datetime(data['Date'], format='%m-%d-%Y %H:%M:%S.%f', utc=True)

######################## AVEC MON GN LOCAL #############################
#data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True) 
########################################################################

data.sort_values(by="Date", inplace=True)
data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
data['Year']=0
for i in range(len(data)):
    data.loc[i,'Year']=datetime.date(data.loc[i,'Date']).year

data_bis =data.copy()
data_bis.set_index('Date', inplace=True)
data_resampled =data_bis.resample(rule="3D").size()
liste_dates = data_resampled.index.values
liste_comptes = data_resampled.values
df = pd.DataFrame([liste_dates,liste_comptes], index=['Date','Compte_mensuel']).T
df['Date'] = pd.to_datetime(df['Date'], format='mixed', utc=True)
for i in range(len(df)):
    df.loc[i,'Year']=datetime.date(df.loc[i,'Date']).year

start_date_year = data['Year'].iloc[0]
end_date_year = data['Year'].iloc[-1]
nb_enregistrements = len(data)
##################################### TRAITEMENT PREALABLE MAP ###################################
data['long']=0
data['lat']=0

for i in range(len(data)):
    try:
        l = re.split(']',data['location'][i])
        l2 = l[0][20:]
        l3 = re.split(',',l2)
        long_i = l3[0]
        lat_i = l3[1]
        try:
            data.loc[i,'lat']=float(lat_i.replace('\n','').replace(" ",''))
        except:
            data.loc[i,'lat']=""
        try:
            data.loc[i,'long']=float(long_i.replace('\n','').replace(" ",''))
        except:
            data.loc[i,'long']=""
    except:
        pass

#################################### AVEC MON GN LOCAL ##########################################
#data['location'].astype(str)
#for i in range(len(data)):
#    try:
#        lat_i = float(re.split(",", data['location'].iloc[i])[0].replace('"','').replace('[',''))
#        data['lat'].iloc[i]=lat_i
#    except:
#        pass
#    try:
#       long_i = float(re.split(",", data['location'].iloc[i])[1].replace('"','').replace('[',''))
#        data['long'].iloc[i]=long_i
#    except:
#        pass
##################################################################################################

data.to_csv("pages/data/Data_ready.csv")
