import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
pd.options.mode.chained_assignment = None

##################################### LECTURE DATA ###########################################
data = pd.read_csv("pages/data/Enregistrements_RZA_060524.csv")
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

#########################################  TRAITEMENT MOTS CLES / FILTRE ZA ############################################

data_ =data.drop(columns=['Date','location','Org',"resourceTitleObject.default","cl_useConstraints.default",'uuid','format','owner','recordOwner',"standardNameObject.default"])

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

rechercheZAA = [' zaa']
rechercheZAAJ = ['zaaj']
rechercheZAAR = ['zaar']
rechercheZAEU = ['zaeu']
rechercheZAS = ['zas']
rechercheZAM = ['zam']
rechercheZABRI = ['zabri']
rechercheZABR = ['zabr']
rechercheZAL = ['zal']
rechercheZAPygar = ['zapygar']

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

dat = pd.concat([data,data_bis], axis=1)

#######################################

dat['Year']=0
for i in range(len(dat)):
    dat.loc[i,'Year']=datetime.date(dat.loc[i,'Date']).year

start_date_year = dat['Year'].iloc[0]
end_date_year = dat['Year'].iloc[-1]

##################################### TRAITEMENT PREALABLE MAP ###################################
dat['long']=0
dat['lat']=0

for i in range(len(dat)):
    try:
        l = re.split(']',dat['location'][i])
        l2 = l[0][20:]
        l3 = re.split(',',l2)
        long_i = l3[0]
        lat_i = l3[1]
        try:
            dat.loc[i,'lat']=float(lat_i.replace('\n','').replace(" ",''))
        except:
            dat.loc[i,'lat']=""
        try:
            dat.loc[i,'long']=float(long_i.replace('\n','').replace(" ",''))
        except:
            dat.loc[i,'long']=""
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

for i in range(len(dat)):
    if dat.loc[i,'format']=='-':
        dat.loc[i,'format']='non renseigné'

for i in range(len(dat)):
    try:
        l = dat.loc[i,'format']
        dat.loc[i,'format']=re.split(',',l)[0].replace('.','').lower().replace('excel','xls')
        if dat.loc[i,'format']=='shape':
            dat.loc[i,'format']='esri shapefile'
        if dat.loc[i,'format']=='shp':
            dat.loc[i,'format']='esri shapefile'
        if dat.loc[i,'format']=='shapefile':
            dat.loc[i,'format']='esri shapefile'
        if dat.loc[i,'format']=='esri shapefile (shp)':
            dat.loc[i,'format']='esri shapefile'
        if dat.loc[i,'format']=='shapefile (shp)':
            dat.loc[i,'format']='esri shapefile'
        if dat.loc[i,'format']=='xlsx':
            dat.loc[i,'format']='xls'
        if dat.loc[i,'format']=='tif':
            dat.loc[i,'format']='geotiff'
        if dat.loc[i,'format']=='tiff':
            dat.loc[i,'format']='geotiff'
        if dat.loc[i,'format']=='texte':
            dat.loc[i,'format']='txt'
        if dat.loc[i,'format']=='jpeg2000':
            dat.loc[i,'format']='jpeg'
        if dat.loc[i,'format']=='jpg':
            dat.loc[i,'format']='jpeg'
        if dat.loc[i,'format']=='application/pdf':
            dat.loc[i,'format']='pdf'
    except:
        pass

for i in range(len(dat)):
    if dat.loc[i,'Org']=='-':
        dat.loc[i,'Org']='non renseigné'

for i in range(len(dat)):
    try:
        l = dat.loc[i,'Org']
        dat.loc[i,'Org']=re.split(',',l)[0].lower()
        if dat.loc[i,'Org']=='letg umr 6554 cnrs':
            dat.loc[i,'Org']='umr6554 letg cnrs'
        if dat.loc[i,'Org']=='letg-rennes costelletg-rennes umr 6554 cnrs université de rennes 2':
            dat.loc[i,'Org']='umr6554 letg cnrs'
        if dat.loc[i,'Org']=='letg rennes umr 6554 cnrs université de rennes 2':
            dat.loc[i,'Org']='umr6554 letg cnrs'
        if dat.loc[i,'Org']=='sorbonne université - metis':
            dat.loc[i,'Org']='umr 7619 metis sorbonne université'
        if dat.loc[i,'Org']=='sorbonne université - umr 7619 metis':
            dat.loc[i,'Org']='umr 7619 metis sorbonne université'
        if dat.loc[i,'Org']=='upmc - umr 7619 metis':
            dat.loc[i,'Org']='umr 7619 metis sorbonne université'
        if dat.loc[i,'Org']=='sorbonne université - métis':
            dat.loc[i,'Org']='umr 7619 metis sorbonne université'
        if dat.loc[i,'Org']=='upsorbonne université - umr 7619 metis':
            dat.loc[i,'Org']='umr 7619 metis sorbonne université'
        if dat.loc[i,'Org']=='cnrs - eccorev (fr3098)':
            dat.loc[i,'Org']='eccorev (fr3098) - cnrs'
        if dat.loc[i,'Org']=='cnrs - eccorev (fr3098) - ohm bassin minier de provence':
            dat.loc[i,'Org']='eccorev (fr3098) - cnrs'
        if dat.loc[i,'Org']=='letg-rennes costel':
            dat.loc[i,'Org']='umr6554 letg cnrs'
        if dat.loc[i,'Org']=='ietr umr cnrs 6164 / letg-rennes umr 6554 cnrs université de rennes 2':
            dat.loc[i,'Org']='umr6554 letg cnrs'
        if dat.loc[i,'Org']=='letg':
            dat.loc[i,'Org']='umr6554 letg cnrs'
        if dat.loc[i,'Org']=='letg-rennes umr 6554 cnrs université de rennes 2' :
            dat.loc[i,'Org']='umr6554 letg cnrs'            
        if dat.loc[i,'Org']=="umr 1069 sas inrae - l'institut agro rennes-angers":
            dat.loc[i,'Org']='umr 1069 sas inra - agrocampus ouest'
        if dat.loc[i,'Org']=='ens de lyon - umr 5600 evs' :
            dat.loc[i,'Org']='umr 5600 evs - ens de lyon'
        if dat.loc[i,'Org']=='evs umr 5600 cnrs université de lyon' :
            dat.loc[i,'Org']='umr 5600 evs - ens de lyon'
        if dat.loc[i,'Org']=='umr 5600' :
            dat.loc[i,'Org']='umr 5600 evs - ens de lyon'    
        if dat.loc[i,'Org']=='cnrs leca' :
            dat.loc[i,'Org']='leca' 
        if dat.loc[i,'Org']=='ecobio umr 6553 cnrs université de rennes 1' :
            dat.loc[i,'Org']='ecobio umr 6553'
        if dat.loc[i,'Org']=='ecobio umr 6553 cnrs université de rennes' :
            dat.loc[i,'Org']='ecobio umr 6553'
        if dat.loc[i,'Org']=='umr 6553 cnrs ecobio' :
            dat.loc[i,'Org']='ecobio umr 6553'
        if dat.loc[i,'Org']=='umr 6553 ecobio' :
            dat.loc[i,'Org']='ecobio umr 6553'
        if dat.loc[i,'Org']=='umr ecobio 6553 cnrs université de rennes 1' :
            dat.loc[i,'Org']='ecobio umr 6553'
        if dat.loc[i,'Org']=='bagap umr 0980' :
            dat.loc[i,'Org']='bagap umr 0980 inrae agrocampus'
        if dat.loc[i,'Org']=='inrae bagap' :
            dat.loc[i,'Org']='bagap umr 0980 inrae agrocampus'
        if dat.loc[i,'Org']=='bagap umr 0980 inrae agrocampus ouest esa' :
            dat.loc[i,'Org']='bagap umr 0980 inrae agrocampus'
        if dat.loc[i,'Org']=='mines saint-etienne - centre spin - peg' :
            dat.loc[i,'Org']='mines saint-etienne - centre spin'
        if dat.loc[i,'Org']=='mines saint-etienne' :
            dat.loc[i,'Org']='mines saint-etienne - centre spin'
        if dat.loc[i,'Org']=='mines saint-etienne - centre spn - gse' :
            dat.loc[i,'Org']='mines saint-etienne - centre spin'
        if dat.loc[i,'Org']=='irstea grenoble - ur dtm' :
            dat.loc[i,'Org']='irstea grenoble'
        if dat.loc[i,'Org']=='irstea' :
            dat.loc[i,'Org']='irstea grenoble' 
        if dat.loc[i,'Org']=='espace umr 7300 cnrs uma' :
            dat.loc[i,'Org']='umr 7300 espace cnrs'
        if dat.loc[i,'Org']=='espace umr 7300 cnrs au' :
            dat.loc[i,'Org']='umr 7300 espace cnrs'
        if dat.loc[i,'Org']=='inra' :
            dat.loc[i,'Org']='umr 1069 sas inra - agrocampus ouest'
    except:
        pass

dat.to_csv("pages/data/Data_ready.csv")