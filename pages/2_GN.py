import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

pd.options.mode.chained_assignment = None

st.title("Analyse des catalogues")

liste_ZAs= ['ZA1','ZA2','ZA3']
Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs)

##################################### LECTURE DATA ###########################################
data = pd.read_csv("pages\data\Enregistrements_190424.csv")

##################################### TRAITEMENT PREALABLE ###################################
data_dates=data[["createDate"]]
data_dates.rename(columns={"createDate":"Date"}, inplace=True)
nb_enregistrements = len(data_dates)
data_dates.dropna(subset="Date" ,inplace=True)
data_dates['Date'] = pd.to_datetime(data_dates['Date'], format='mixed', utc=True)
data_dates.sort_values(by="Date", inplace=True)
data_dates.loc[:,'Compte']=np.arange(len(data_dates))+1
data_dates['Year']=0
for i in range(len(data_dates)):
    data_dates.loc[i,'Year']=datetime.date(data_dates.loc[i,'Date']).year
#data_dates.set_index('Date', inplace=True)

start_date_year = data_dates['Year'].iloc[0]
end_date_year = data_dates['Year'].iloc[-1]

###################################### VISUALISATION #########################################
with st.container(border=True):
    row1 = st.columns(2)

    with row1[0]:
        selection_dates = st.slider('Zoomer sur une période plus récente',min_value=start_date_year,max_value=end_date_year)
        nb_enregistrements = len(data_dates[data_dates.Year >= selection_dates])
        st.scatter_chart(data=data_dates[data_dates.Year >= selection_dates], x='Date', y='Compte',height=300)
    
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


with st.container(border=True):
    row2 = st.columns(2)

    with row2[0]:
        st.write('à remplir')
    with row2[1]:
        st.write('à remplir')