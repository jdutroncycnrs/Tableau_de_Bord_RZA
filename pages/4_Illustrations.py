import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
pd.options.mode.chained_assignment = None


########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Illustrations",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

######################################################################## Attention les ZA et OHM à sélectionner inscrits en dur ###############
liste_ZAs= ['ZAA','ZAAJ','ZAAR','ZAEU','ZABR','ZABRI','ZAM','ZAL','ZAS','ZAPygar']
liste_OHMs =['OHM_BMProvence','OHMI_Tessekere','OHM_Pyrenees','OHM_VRhone','OHMI_Pima','OHMI_Estarreja','OHM_Mediterraneen','OHM_Oyapock','OHMI_Nunavik','OHM_Caraibes','OHM_PDBitche','OHMI_Patagonia','OHM_Fessenheim']


###################### SELECTION SIDEBAR ######################################################################################################
all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs
    Selection_OHM = []
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs)
    OHMs= st.sidebar.checkbox("Pour filtrer un OHM")
    if OHMs==False:
        Selection_OHM= st.sidebar.multiselect(label="OHMs", options=liste_OHMs, disabled=True)
    else:
        Selection_OHM= st.sidebar.multiselect(label="OHMs", options=liste_OHMs)

########################## TRANSFORMATION SELECTION EN STRING POUR CERTAINS AFFICHAGES #####################""""
if len(Selection_ZA)>0:
    Selection_ZA_str = Selection_ZA[0]
    for i in range(1,len(Selection_ZA)):
        Selection_ZA_str+="+" + Selection_ZA[i]

if len(Selection_OHM)>0:
    Selection_OHM_str = Selection_OHM[0]
    for i in range(1,len(Selection_OHM)):
        Selection_OHM_str+="+" + Selection_OHM[i]

###################################### LECTURE DATA NETTOYEES #########################################
####### FICHIER A LIRE ####################
fichier= 'Enregistrements_RZA_220524_ready'
dat = pd.read_csv(f"pages/data/{fichier}.csv")
dat['Date'] = pd.to_datetime(dat['Date'], format='mixed', utc=True)
dat.sort_values(by="Date", inplace=True)
#dat['Datestamp'] = pd.to_datetime(dat['Datestamp'], format='mixed', utc=True)
#dat.sort_values(by="Datestamp", inplace=True)
for i in range(len(dat)):
    dat.loc[i,'Year']=datetime.date(dat.loc[i,'Date']).year

###################################### FILTRAGE ZA ###################################################
if len(Selection_ZA)==1:
    data = dat[dat[Selection_ZA[0]]==1]
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==2:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==3:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==4:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==5:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==6:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==7:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==8:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==9:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1],dat[dat[Selection_ZA[8]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==10:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1],dat[dat[Selection_ZA[8]]==1],dat[dat[Selection_ZA[9]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==1:
    data = dat[dat[Selection_OHM[0]]==1]
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==2:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==3:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==4:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==5:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==6:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1],dat[dat[Selection_OHM[5]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==7:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1],dat[dat[Selection_OHM[5]]==1],dat[dat[Selection_OHM[6]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==8:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1],dat[dat[Selection_OHM[5]]==1],dat[dat[Selection_OHM[6]]==1],dat[dat[Selection_OHM[7]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==9:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1],dat[dat[Selection_OHM[5]]==1],dat[dat[Selection_OHM[6]]==1],dat[dat[Selection_OHM[7]]==1],dat[dat[Selection_OHM[8]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==10:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1],dat[dat[Selection_OHM[5]]==1],dat[dat[Selection_OHM[6]]==1],dat[dat[Selection_OHM[7]]==1],dat[dat[Selection_OHM[8]]==1],dat[dat[Selection_OHM[9]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
else:
    data = dat.copy()
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data['Datestamp'] = pd.to_datetime(dat['Datestamp'], format='mixed', utc=True)
    #data.sort_values(by="Datestamp", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
#######################################################################################################

piq_one_check = st.sidebar.checkbox("Selection d'un enregistrement unique")

date_fichier = st.sidebar.markdown(f'Le fichier utilisé : {fichier}')

data_test = data.copy()
colors = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0','#F9A2BF','#3E9399','#3D4A81','#ECDCC5','#D2CFC8']

len_zas= []
for za in Selection_ZA:
    len_zas.append(len(data_test[data_test[za]==1]))
    
fig8=go.Figure()
for i, za in enumerate(Selection_ZA):
    selec = Selection_ZA[i:i+1]
    selec_len = len_zas[i:i+1]
    fig8.add_trace(go.Bar(
                x=selec,
                y=selec_len,
                name=za,
                marker=dict(color=colors[i])
            ))
fig8.update_layout(
                        title='Nombre de fiches répertoriées au 06/06/24',
                        width=1000,
                        height=500)
st.plotly_chart(fig8)