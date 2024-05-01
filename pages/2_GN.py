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
data = pd.read_csv("pages/data/Enregistrements_190424.csv")
data.rename(columns={"createDate":"Date"}, inplace=True)

##################################### TRAITEMENT PREALABLE DATES###################################
data_dates=data[["Date"]]
nb_enregistrements = len(data_dates)
data_dates.dropna(subset="Date" ,inplace=True)
data_dates['Date'] = pd.to_datetime(data_dates['Date'], format='mixed', utc=True)
data_dates.sort_values(by="Date", inplace=True)
data_dates.loc[:,'Compte_cumulé']=np.arange(len(data_dates))+1
data_dates['Year']=0
for i in range(len(data_dates)):
    data_dates.loc[i,'Year']=datetime.date(data_dates.loc[i,'Date']).year

data_dates_bis =data_dates.copy()
data_dates_bis.set_index('Date', inplace=True)
data_dates_resampled =data_dates_bis.resample(rule="ME").size()
liste_dates = data_dates_resampled.index.values
liste_comptes = data_dates_resampled.values
df = pd.DataFrame([liste_dates,liste_comptes], index=['Date','Compte_mensuel']).T
df['Date'] = pd.to_datetime(df['Date'], format='mixed', utc=True)
for i in range(len(df)):
    df.loc[i,'Year']=datetime.date(df.loc[i,'Date']).year

start_date_year = data_dates['Year'].iloc[0]
end_date_year = data_dates['Year'].iloc[-1]

##################################### TRAITEMENT PREALABLE MAP ###################################
data['long']=0
data['lat']=0
data_maps = data.drop(columns=['Org','popularity','resourceType','uuid'])
data_maps.dropna(subset= 'location', inplace=True)
data_maps['location'].astype(str)
for i in range(len(data_maps)):
    if data_maps['location'].iloc[i][0]=="0":
        data_maps['location'].iloc[i]=np.NaN
data_maps.dropna(subset= 'location', inplace=True)
for i in range(len(data_maps)):
    lat_i = float(re.split(",", data_maps['location'].iloc[i])[0].replace('"','').replace('[',''))
    long_i = float(re.split(",", data_maps['location'].iloc[i])[1].replace('"','').replace('[',''))
    data_maps['lat'].iloc[i]=lat_i
    data_maps['long'].iloc[i]=long_i

###################################### VISUALISATION #########################################
st.subheader('Evolution temporelle')
with st.container(border=True):
    row1 = st.columns(2)

    with row1[0]:
        selection_dates = st.slider('Zoomer sur une période plus récente',min_value=start_date_year,max_value=end_date_year)
        nb_enregistrements = len(data_dates[data_dates.Year >= selection_dates])
        st.scatter_chart(data=data_dates[data_dates.Year >= selection_dates], x='Date', y='Compte_cumulé',height=300)
    
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
        st.write('à remplir')
        st.map(data_maps[data_maps['lat']>35][data_maps['long']<6],latitude='lat',longitude='long',zoom=4.5)
    with row2[1]:
        st.write('à remplir')