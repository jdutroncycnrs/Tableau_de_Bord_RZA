import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
pd.options.mode.chained_assignment = None

##################################### LECTURE DATA ###########################################
fichier = 'Enregistrements_RZA_220524'
data = pd.read_csv(f"pages/data/{fichier}.csv")
data.rename(columns={"createDate":"Date"}, inplace=True)
data.rename(columns={"dateStamp":"Datestamp"}, inplace=True)
data.rename(columns={"changeDate":"Date_changement"}, inplace=True)
data.rename(columns={"creationDateForResource":"CreationDate"}, inplace=True)
data.rename(columns={"revisionDateForResource":"RevisionDate"}, inplace=True)
data.rename(columns={"publicationDateForResource":"PublicationDate"}, inplace=True)

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
        data.loc[i,'Datestamp'] = data.loc[i,'Datestamp'].replace(term,num).replace('@','/')
        data.loc[i,'CreationDate'] = data.loc[i,'CreationDate'].replace(term,num).replace('@','/')
        data.loc[i,'RevisionDate'] = data.loc[i,'RevisionDate'].replace(term,num).replace('@','/')
        data.loc[i,'PublicationDate'] = data.loc[i,'PublicationDate'].replace(term,num).replace('@','/')
    for term, num in dico2.items():
        data.loc[i,'Date'] = data.loc[i,'Date'].replace(term,num).replace(',','')
        data.loc[i,'Datestamp'] = data.loc[i,'Datestamp'].replace(term,num).replace(',','')
        data.loc[i,'CreationDate'] = data.loc[i,'CreationDate'].replace(term,num).replace(',','')
        data.loc[i,'RevisionDate'] = data.loc[i,'RevisionDate'].replace(term,num).replace(',','')
        data.loc[i,'PublicationDate'] = data.loc[i,'PublicationDate'].replace(term,num).replace(',','')
    data.loc[i,'Date'] = re.split('/',data.loc[i,'Date'])[0][0:-1].replace(' ','-')+re.split('/',data.loc[i,'Date'])[1]
    try:
        data.loc[i,'Datestamp'] = re.split('/',data.loc[i,'Datestamp'])[0][0:-1].replace(' ','-')+re.split('/',data.loc[i,'Datestamp'])[1]
    except:
        pass
    try:
        data.loc[i,'CreationDate'] = re.split('/',data.loc[i,'CreationDate'])[0][0:-1].replace(' ','-')+re.split('/',data.loc[i,'CreationDate'])[1]
    except:
        pass
    try:
        data.loc[i,'RevisionDate'] = re.split('/',data.loc[i,'RevisionDate'])[0][0:-1].replace(' ','-')+re.split('/',data.loc[i,'RevisionDate'])[1]
    except:
        pass
    try:
        data.loc[i,'PublicationDate'] = re.split('/',data.loc[i,'PublicationDate'])[0][0:-1].replace(' ','-')+re.split('/',data.loc[i,'PublicationDate'])[1]
    except:
        pass

data['Date'] = pd.to_datetime(data['Date'], format='%m-%d-%Y %H:%M:%S.%f', utc=True)

for i in range(len(data)):
    try:
        data.loc[i,'Datestamp'] = pd.to_datetime(data.loc[i,'Datestamp'], format='mixed', utc=True)
    except:
        data.loc[i,'Datestamp'] = np.NaN
for i in range(len(data)):
    try:
        data.loc[i,'CreationDate'] = pd.to_datetime(data.loc[i,'CreationDate'], format='mixed', utc=True)
    except:
        data.loc[i,'CreationDate'] = np.NaN
for i in range(len(data)):
    try:
        data.loc[i,'RevisionDate'] = pd.to_datetime(data.loc[i,'RevisionDate'], format='mixed', utc=True)
    except:
        data.loc[i,'RevisionDate'] = np.NaN
for i in range(len(data)):
    try:
        data.loc[i,'PublicationDate'] = pd.to_datetime(data.loc[i,'PublicationDate'], format='mixed', utc=True)
    except:
        data.loc[i,'PublicationDate'] = np.NaN

######################## AVEC MON GN LOCAL #############################
#data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True) 
########################################################################

#########################################  TRAITEMENT MOTS CLES / FILTRE ZA ############################################
data_mots_cles = data.copy()

data_mots_cles.drop(columns=['cl_topic.default','cl_status.default','cl_hierarchyLevel.default','cl_accessConstraints.default','cl_useConstraints.default','resourceTitleObject.default','Date','Datestamp','RevisionDate','PublicationDate','CreationDate','groupPublished','popularity','location','Org','format','uuid','recordOwner'], inplace=True)
l_to_supp = []

liste_tagNumber_bis = []
for i,x in enumerate(data_mots_cles.columns):
    if 'Number' in data_mots_cles.columns[i]:
        liste_tagNumber_bis.append(x)
data_mots_cles.drop(columns=liste_tagNumber_bis, inplace=True)
for j in range(len(data_mots_cles)):
    try:
        data_mots_cles.loc[j,'mot_clés']=data_mots_cles.loc[j,data_mots_cles.columns[0]]
        try:
            for c in range(1,len(data_mots_cles.columns)):
                data_mots_cles.loc[j,'mot_clés'] +=',' + data_mots_cles.loc[j,data_mots_cles.columns[c]].replace('^',' ')
        except:
            pass
    except:
        pass
print(len(data_mots_cles.columns))

data_ = pd.concat([data,data_mots_cles['mot_clés']],axis=1)

print(data_.head())
print(data_.columns.values)

##############################################################################################################################

data_to_filter =data_[['groupPublished','mot_clés']]

data_to_filter['filtre']=data_to_filter['groupPublished']+data_to_filter['mot_clés']
df = pd.DataFrame(index=data.index,columns=['ZAA','ZAAJ','ZAAR','ZAEU','ZAS','ZAM','ZABRI','ZABR','ZAL','ZAPygar','OHM_BMProvence','OHMI_Tessekere','OHM_Pyrenees','OHM_VRhone','OHMI_Pima','OHMI_Estarreja','OHM_Mediterraneen','OHM_Oyapock','OHMI_Nunavik','OHM_Caraibes','OHM_PDBitche','OHMI_Patagonia','OHM_Fessenheim'])
data_bis = pd.concat([data_to_filter,df],axis=1)

print(re.split(',',data_bis.loc[0,'filtre'])[0])

rechercheZAA = ['zaa']
rechercheZAAJ = ['zaaj']
rechercheZAAR = ['zaar']
rechercheZAEU = ['zaeu']
rechercheZAS = ['zas']
rechercheZAM = ['zam']
rechercheZABRI = ['zabri']
rechercheZABR = ['zabr']
rechercheZAL = ['zal']
rechercheZAPygar = ['zapygar']
rechercheOHMbmp = ['ohm_bmp']
rechercheOHMITES = ['ohmi_tes']
rechercheOHMHV = ['ohm_hv']
rechercheOHMVR = ['ohm_vr']
rechercheOHMIPIC = ['ohmi_pic']
rechercheOHMIEST = ['ohmi_est']
rechercheOHMLM = ['ohm_lm']
rechercheOHMOY = ['ohm_oyapock']
rechercheOHMINUN = ['ohmi_nun']
rechercheOHMCAR = ['ohm_car']
rechercheOHMPDB = ['ohm_pdb']
rechercheOHMIPata = ['ohmi_pata']
rechercheOHMFES = ['ohm_fes']

for i in range(len(data_bis)):
    lis = re.split(',',data_bis.loc[i,'groupPublished'])
    for u in lis:
        if u.strip().lower() in rechercheZAA:
            data_bis.loc[i,'ZAA']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheZAAJ:
            data_bis.loc[i,'ZAAJ']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheZAAR:
            data_bis.loc[i,'ZAAR']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheZAEU:
            data_bis.loc[i,'ZAEU']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheZAS:
            data_bis.loc[i,'ZAS']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheZAM:
            data_bis.loc[i,'ZAM']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheZABRI:
            data_bis.loc[i,'ZABRI']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheZABR:
            data_bis.loc[i,'ZABR']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheZAL:
            data_bis.loc[i,'ZAL']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheZAPygar:
            data_bis.loc[i,'ZAPygar']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMbmp:
            data_bis.loc[i,'OHM_BMProvence']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMITES:
            data_bis.loc[i,'OHMI_Tessekere']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMHV:
            data_bis.loc[i,'OHM_Pyrenees']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMVR:
            data_bis.loc[i,'OHM_VRhone']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMIPIC:
            data_bis.loc[i,'OHMI_Pima']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMIEST:
            data_bis.loc[i,'OHMI_Estarreja']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMLM:
            data_bis.loc[i,'OHM_Mediterraneen']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMOY:
            data_bis.loc[i,'OHM_Oyapock']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMINUN:
            data_bis.loc[i,'OHMI_Nunavik']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMCAR:
            data_bis.loc[i,'OHM_Caraibes']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMPDB:
            data_bis.loc[i,'OHM_PDBitche']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMIPata:
            data_bis.loc[i,'OHMI_Patagonia']=1
        else:
            pass
    for u in lis:
        if u.strip().lower() in rechercheOHMFES:
            data_bis.loc[i,'OHM_Fessenheim']=1
        else:
            pass

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
print('OHM_BMProvence',len(data_bis['OHM_BMProvence'][data_bis['OHM_BMProvence']==1]))
print('OHMI_Tessekere',len(data_bis['OHMI_Tessekere'][data_bis['OHMI_Tessekere']==1]))
print('OHM_Pyrenees',len(data_bis['OHM_Pyrenees'][data_bis['OHM_Pyrenees']==1]))
print('OHM_VRhone',len(data_bis['OHM_VRhone'][data_bis['OHM_VRhone']==1]))
print('OHMI_Pima',len(data_bis['OHMI_Pima'][data_bis['OHMI_Pima']==1]))
print('OHMI_Estarreja',len(data_bis['OHMI_Estarreja'][data_bis['OHMI_Estarreja']==1]))
print('OHM_Mediterraneen',len(data_bis['OHM_Mediterraneen'][data_bis['OHM_Mediterraneen']==1]))
print('OHM_Oyapock',len(data_bis['OHM_Oyapock'][data_bis['OHM_Oyapock']==1]))
print('OHMI_Nunavik',len(data_bis['OHMI_Nunavik'][data_bis['OHMI_Nunavik']==1]))
print('OHM_Caraibes',len(data_bis['OHM_Caraibes'][data_bis['OHM_Caraibes']==1]))
print('OHM_PDBitche',len(data_bis['OHM_PDBitche'][data_bis['OHM_PDBitche']==1]))
print('OHMI_Patagonia',len(data_bis['OHMI_Patagonia'][data_bis['OHMI_Patagonia']==1]))
print('OHM_Fessenheim',len(data_bis['OHM_Fessenheim'][data_bis['OHM_Fessenheim']==1]))

dat = pd.concat([data_,data_bis], axis=1)
print(dat.columns.values)
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
        if dat.loc[i,'format']=='application/vndms-xls':
            dat.loc[i,'format']='xls'
        if dat.loc[i,'format']=='application/msword':
            dat.loc[i,'format']='doc'
        if dat.loc[i,'format']=='application/vndopenxmlformats-officedocumentspreadsheetmlsheet':
            dat.loc[i,'format']='xls'
        if dat.loc[i,'format']=='application/x-shapefile':
            dat.loc[i,'format']='esri shapefile'
        if dat.loc[i,'format']=='application/vndoasisopendocumenttext':
            dat.loc[i,'format']='doc'
        if dat.loc[i,'format']=='application/vndgoogle-earthkml+xml':
            dat.loc[i,'format']='autre'
        if dat.loc[i,'format']=='application/vndfddsnmseed':
            dat.loc[i,'format']='autre'
        if dat.loc[i,'format']=='orthophotos et orthomosaïques = geotiff images individuelles rvb = jpeg ; irt = tiff':
            dat.loc[i,'format']='geotiff'
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
        if dat.loc[i,'Org']=='ecole des mines de saint-etienne- umr 5600 evs' :
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
            dat.loc[i,'Org']='irstea'
        if dat.loc[i,'Org']=='irstea lyon-villeurbanne' :
            dat.loc[i,'Org']='irstea' 
        if dat.loc[i,'Org']=='espace umr 7300 cnrs uma' :
            dat.loc[i,'Org']='umr 7300 espace cnrs'
        if dat.loc[i,'Org']=='espace umr 7300 cnrs au' :
            dat.loc[i,'Org']='umr 7300 espace cnrs'
        if dat.loc[i,'Org']=='umr espace 7300' :
            dat.loc[i,'Org']='umr 7300 espace cnrs'
        if dat.loc[i,'Org']=='inra' :
            dat.loc[i,'Org']='umr 1069 sas inra - agrocampus ouest'
        if dat.loc[i,'Org']=='zaa-ltser' :
            dat.loc[i,'Org']='zaa'
        if dat.loc[i,'Org']=="direction régionale de l’environnement de l’aménagement et du logement d'auvergne-rhône-alpes (dreal auvergne-rhône-alpes)" :
            dat.loc[i,'Org']='dreal'
        if dat.loc[i,'Org']=="asters - cen 74" :
            dat.loc[i,'Org']='asters cen 74'
    except:
        pass

for i in range(len(dat)):
    if dat.loc[i,'cl_topic.default']=='-':
        dat.loc[i,'cl_topic.default']='non renseigné'

for i in range(len(dat)):
    if dat.loc[i,'cl_useConstraints.default']=='-':
        dat.loc[i,'cl_useConstraints.default']='non renseigné'

for i in range(len(dat)):
    l = dat.loc[i,'cl_useConstraints.default']
    dat.loc[i,'cl_useConstraints.default']=re.split(',',l)[0].strip().lower()
    if dat.loc[i,'cl_useConstraints.default']=='license':
        dat.loc[i,'cl_useConstraints.default']='licence'
    if dat.loc[i,'cl_useConstraints.default']=='license_ use:licence cc-by':
        dat.loc[i,'cl_useConstraints.default']='licence cc-by'
    if dat.loc[i,'cl_useConstraints.default']=='otherrestictions':
        dat.loc[i,'cl_useConstraints.default']='other restrictions'

for i in range(len(dat)):
    l = dat.loc[i,'cl_status.default']
    dat.loc[i,'cl_status.default']=re.split(',',l)[0].strip().lower()
    if dat.loc[i,'cl_status.default']=='-':
        dat.loc[i,'cl_status.default']='non renseigné'
    if dat.loc[i,'cl_status.default']=='underdevelopment':
        dat.loc[i,'cl_status.default']='under development'


for i,x in enumerate(dat.columns):
    if 'Number' in dat.columns[i]:
            for u in range(len(dat)):
                if dat.loc[u,dat.columns[i]]=="0":
                    dat.loc[u,dat.columns[i]]="-"

for i in range(len(dat)):
    try:
        l1 = re.split(':',dat.loc[i,'contact'])[7]
        dat.loc[i,'contact']=re.split(',',l1)[0].replace('"','').replace('[','').replace(']','')
    except:
        pass

dat.to_csv(f"pages/data/{fichier}_ready.csv")