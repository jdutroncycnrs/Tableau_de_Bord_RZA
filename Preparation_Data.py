import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
pd.options.mode.chained_assignment = None

##################################### LECTURE DATA ###########################################
data = pd.read_csv("pages/data/Enregistrements_RZA_030524-2.csv")
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

start_date_year = data['Year'].iloc[0]
end_date_year = data['Year'].iloc[-1]

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

data_ =data.drop(columns=['Date','location','Compte_cumulé','Year','long','lat'])

liste_columns_data = data_.columns.values

for c in liste_columns_data:
    for i in range(len(data_)):
        l = data_.loc[i,c]
        data_.loc[i,c] = re.split(',',l)

data_.to_csv('temp/data')

data2 = pd.read_csv('temp/data')
data2.drop(columns=['Unnamed: 0'], inplace=True)

liste_index= data2.index.values
liste_columns_data2 = data2.columns.values
data_bis = pd.DataFrame(index=liste_index,columns=['ZAA','ZAAJ','ZAAR','ZAEU','ZAS','ZAM','ZABRI','ZABR','ZAL','ZAPygar'])

rechercheZAA = ['ZAA', 'Zone Atelier Alpes']
rechercheZAAJ = ['ZAAJ', 'Zone Atelier Arc Jurassien']
rechercheZAAR = ['ZAAR', 'Zone Atelier Armorique']
rechercheZAEU = ['ZAEU', 'Zone Atelier Environnementale Urbaine']
rechercheZAS = ['ZAS','Zone Atelier Seine']
rechercheZAM = ['ZAM', 'Zone Atelier Moselle']
rechercheZABRI = ['ZABRI','Zone Atelier Brest Iroise']
rechercheZABR = ['ZABR','Zone Atelier Bassin du Rhone']
rechercheZAL = ['ZAL','Zone Atelier Loire']
rechercheZAPygar = ['ZAPygar', 'Zone Atelier Pyrénées Garonne' ]

for c in liste_columns_data2:
    for i in range(len(data2)):
        lis = data2.loc[i,c]
        for u in rechercheZAA:
            if u in lis:
                data_bis.loc[i,'ZAA']=1
            else:
                pass
        for u in rechercheZAAJ:
            if u in lis:
                data_bis.loc[i,'ZAAJ']=1
            else:
                pass
        for u in rechercheZAAR:
            if u in lis:
                data_bis.loc[i,'ZAAR']=1
            else:
                pass
        for u in rechercheZAEU:
            if u in lis:
                data_bis.loc[i,'ZAEU']=1
            else:
                pass
        for u in rechercheZAS:
            if u in lis:
                data_bis.loc[i,'ZAS']=1
            else:
                pass
        for u in rechercheZAM:
            if u in lis:
                data_bis.loc[i,'ZAM']=1
            else:
                pass
        for u in rechercheZABRI:
            if u in lis:
                data_bis.loc[i,'ZABRI']=1
            else:
                pass
        for u in rechercheZABR:
            if u in lis:
                data_bis.loc[i,'ZABR']=1
            else:
                pass
        for u in rechercheZAL:
            if u in lis:
                data_bis.loc[i,'ZAL']=1
            else:
                pass
        for u in rechercheZAPygar:
            if u in lis:
                data_bis.loc[i,'ZAPygar']=1
            else:
                pass

data_bis.to_csv('temp/data_bis')

print('ZAA:',len(data_bis['ZAA'][data_bis['ZAA']==1]))
print('ZAAJ:',len(data_bis['ZAAJ'][data_bis['ZAAJ']==1]))
print('ZAAR:',len(data_bis['ZAAR'][data_bis['ZAAR']==1]))
print('ZAEU:',len(data_bis['ZAEU'][data_bis['ZAEU']==1]))
print('ZAM:',len(data_bis['ZAM'][data_bis['ZAM']==1]))
print('ZAS:',len(data_bis['ZAS'][data_bis['ZAS']==1]))
print('ZABRI:',len(data_bis['ZABRI'][data_bis['ZABRI']==1]))
print('ZABR:',len(data_bis['ZABR'][data_bis['ZABR']==1]))
print('ZAL:',len(data_bis['ZAL'][data_bis['ZAL']==1]))
print('ZAPygar:',len(data_bis['ZAPygar'][data_bis['ZAPygar']==1]))

test = pd.concat([data,data_bis], axis=1)

test.to_csv("pages/data/Data_ready.csv")
