import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import seaborn as sns
import matplotlib.pyplot as plt
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
liste_ZAs_= ['ZAA','ZAAJ','ZAAR','ZAEU','ZABR','ZABRI','ZAM','ZAL','ZAS','ZAPygar','ZATU','ZAPVS','ZAH','ZARG','ZACAM','ZATA']
liste_ZAs= ['ZAA','ZAAJ','ZAAR','ZAEU','ZABR','ZABRI','ZAM','ZAL','ZAS','ZAPygar']
liste_OHMs =['OHM_BMProvence','OHMI_Tessekere','OHM_Pyrenees','OHM_VRhone','OHMI_Pima','OHMI_Estarreja','OHM_Mediterraneen','OHM_Oyapock','OHMI_Nunavik','OHM_Caraibes','OHM_PDBitche','OHMI_Patagonia','OHM_Fessenheim']


###################### SELECTION SIDEBAR ######################################################################################################
all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
    Selection_OHM = []
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)
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
fichier= 'Enregistrements_RZA_020624_ready'
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
elif len(Selection_ZA)==11:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1],dat[dat[Selection_ZA[8]]==1],dat[dat[Selection_ZA[9]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==12:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1],dat[dat[Selection_ZA[8]]==1],dat[dat[Selection_ZA[9]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1  
elif len(Selection_ZA)==13:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1],dat[dat[Selection_ZA[8]]==1],dat[dat[Selection_ZA[9]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==14:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1],dat[dat[Selection_ZA[8]]==1],dat[dat[Selection_ZA[9]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==15:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1],dat[dat[Selection_ZA[8]]==1],dat[dat[Selection_ZA[9]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    #data.loc[:,'Compte_cumulé']=np.arange(len(data))+1 
elif len(Selection_ZA)==16:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1],dat[dat[Selection_ZA[8]]==1],dat[dat[Selection_ZA[9]]==1],dat[dat[Selection_ZA[10]]==1],dat[dat[Selection_ZA[11]]==1],dat[dat[Selection_ZA[12]]==1],dat[dat[Selection_ZA[13]]==1],dat[dat[Selection_ZA[14]]==1],dat[dat[Selection_ZA[15]]==1]],axis=0)
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
colors2 = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0','grey','grey','grey','grey','grey','grey']
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
                text=selec_len,
                marker=dict(color=colors2[i])
            ))
fig8.update_layout(
                        title='Nombre de fiches répertoriées au 06/06/24',
                        width=1000,
                        height=500)
st.plotly_chart(fig8)


data_url = data.copy()
data_url['index']=np.arange(0,len(data_url))
data_url.set_index('index', inplace=True)
st.write(len(data_url))
st.write(Selection_ZA)
data_columns = data.columns.values
liste_col_link = []
for i,x in enumerate(data_columns):
    if 'link' in data_columns[i]:
        liste_col_link.append(x)

data_link = data_url[liste_col_link]
l=['linkUrlProtocolDOI','linkUrl','linkProtocol','linkUrlProtocol','linkUrlProtocoldoi',
   'linkUrlProtocolESRIArcGIShttpconfiguration','linkUrlProtocolnull','linkUrlProtocolOGCEDR',
   'linkUrlProtocolOGCWCS','linkUrlProtocolOGCWFS','linkUrlProtocolOGCWFS100httpgetcapabilities',
   'linkUrlProtocolOGCWMS','linkUrlProtocolOGCWMS111httpgetmap','linkUrlProtocolUKST',
   'linkUrlProtocolWWWDOWNLOAD','linkUrlProtocolWWWDOWNLOAD10ftpdownload','linkUrlProtocolWWWDOWNLOAD10httpdownload',
   'linkUrlProtocolWWWLINK','linkUrlProtocolWWWLINK10httplink','linkUrlProtocolWWWLINK10httppartners']

data_link['test']= data_link[l[0]]
for col in l[1:]:
    data_link['test2'] = data_link['test'] + data_link[col]
    data_link['test'] = data_link['test2']

for i in range(len(data_link)):
    try:
        data_link.loc[i,'test']=str(data_link.loc[i,'test']).replace('-','').strip()
    except:
        data_link.loc[i,'test']=''

for i in range(len(data_link)):
    try:
        if "doi" in str(data_link.loc[i,'test']):
            data_link.loc[i,'DOI']=1
        else:
            data_link.loc[i,'DOI']=0
    except:
        data_link.loc[i,'DOI']=0
l0 =[]
for i in range(len(data_link)):
    l1= []
    l1.append(data_link.loc[i,'DOI'])
    l0.append(l1)
fig9 = go.Figure()
fig9.add_trace(go.Heatmap(
    x=['DOI'],
    y=data_link['DOI'].index.values,
    z=l0))
fig9.update_layout(
                title='DOI catalogués',
                yaxis_title='Index',
                width=250,
                height=600)
st.plotly_chart(fig9)

st.write(len(data_link[data_link['DOI']==1.0]))

#st.table(data_link['test'][data_link['DOI']==1.0])

data_link_bis = pd.concat([data_link,data_url['resourceTitleObject.default']], axis=0)
data_link_ter = data[data['resourceTitleObject.default']=="Shapefile de la Zone atelier environnementale urbaine de Strasbourg"]
st.write(data_link_ter['linkUrl'])


fichier2 = "doi"
dat2 = pd.read_csv(f"pages/data/{fichier2}.csv")
dat2.rename(columns={"Unnamed: 2":"Sources"}, inplace=True)

st.dataframe(dat2)

dat2_count = dat2['Sources'].value_counts()
st.write(dat2_count)
fig1= go.Figure()
fig1.add_trace(go.Pie(labels=dat2_count.index.values, values=dat2_count.values))
fig1.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig1.update_layout(
                title='DOI trouvés',
                xaxis_title='Compte',
                yaxis_title='Pointage',
                width=500,
                height=500)
st.plotly_chart(fig1,use_container_width=True)