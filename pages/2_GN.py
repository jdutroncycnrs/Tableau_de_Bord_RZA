import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
pd.options.mode.chained_assignment = None

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Analyse des GN",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

st.title("Analyse des catalogues")

liste_ZAs= ['ZA1','ZA2','ZA3']
Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs)

##################################### LECTURE DATA ###########################################
data = pd.read_csv("pages/data/Enregistrements_RZA_020524.csv")
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

data_maps = data.copy()

###################################### VISUALISATION #########################################
st.subheader('Evolution temporelle')
with st.container(border=True):
    row1 = st.columns(2)

    with row1[0]:
        selection_dates = st.slider('Zoomer sur une période plus récente',min_value=start_date_year,max_value=end_date_year)
        nb_enregistrements = len(data[data.Year >= selection_dates])
        st.scatter_chart(data=data[data.Year >= selection_dates], x='Date', y='Compte_cumulé',height=300)
    
    with row1[1]:
        wch_colour_box = (0,204,102)
        wch_colour_font = (250,250,250)
        fontsize = 25
        valign = "right"
        iconname = "fas fa-asterisk"
        sline = nb_enregistrements
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
        i = "Nombre d'enregistrements"

        htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                    {wch_colour_box[1]}, 
                                                    {wch_colour_box[2]}, 0.75); 
                                color: rgb({wch_colour_font[0]}, 
                                        {wch_colour_font[1]}, 
                                        {wch_colour_font[2]}, 0.75); 
                                font-size: {fontsize}px; 
                                border-radius: 7px; 
                                padding-left: 12px; 
                                padding-top: 18px; 
                                padding-bottom: 18px; 
                                line-height:25px;
                                text-align:center'>
                                <i class='{iconname} fa-xs'></i> {i}
                                </style><BR><span style='font-size: 25px; 
                                margin-top: 0;'>{sline}</style></span></p>"""
        st.markdown(lnk + htmlstr, unsafe_allow_html=True)
        st.bar_chart(data=df[df.Year >= selection_dates], x='Date', y='Compte_mensuel',height=300)

st.subheader('Evolution spatiale')
with st.container(border=True):
    row2 = st.columns(2)

    with row2[0]:
        data_maps = data_maps[data_maps['lat']>45][data_maps['long']<6][data_maps['long']>-6][data.Year >= selection_dates]
        nb_enregistrements_avec_localisation = len(data_maps)
        st.map(data[data['lat']>45][data['long']<6][data['long']>-6][data.Year >= selection_dates],latitude='lat',longitude='long',zoom=4)
    with row2[1]:
        wch_colour_box = (0,204,102)
        wch_colour_font = (250,250,250)
        fontsize = 25
        valign = "right"
        iconname = "fas fa-asterisk"
        sline = nb_enregistrements_avec_localisation
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
        i = "Nombre d'enregistrements localisés sur la carte à gauche"

        htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                    {wch_colour_box[1]}, 
                                                    {wch_colour_box[2]}, 0.75); 
                                color: rgb({wch_colour_font[0]}, 
                                        {wch_colour_font[1]}, 
                                        {wch_colour_font[2]}, 0.75); 
                                font-size: {fontsize}px; 
                                border-radius: 7px; 
                                padding-left: 12px; 
                                padding-top: 18px; 
                                padding-bottom: 18px; 
                                line-height:25px;
                                text-align:center'>
                                <i class='{iconname} fa-xs'></i> {i}
                                </style><BR><span style='font-size: 25px; 
                                margin-top: 0;'>{sline}</style></span></p>"""
        st.markdown(lnk + htmlstr, unsafe_allow_html=True)