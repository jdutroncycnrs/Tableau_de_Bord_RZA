import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
import plotly.express as px
import plotly.graph_objects as go
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

st.title("Analyse des catalogues de cat.InDoRes")

liste_ZAs= ['ZAA','ZAAJ','ZAAR','ZAEU','ZABR','ZABRI','ZAM','ZAL','ZAS','ZAPygar']

Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs)

all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")

if all_ZAs==True:
    Selection_ZA = liste_ZAs

if len(Selection_ZA)>0:
    Selection_ZA_str = Selection_ZA[0]
    for i in range(1,len(Selection_ZA)):
        Selection_ZA_str+="+" + Selection_ZA[i]

###################################### LECTURE DATA NETTOYEES #########################################
dat = pd.read_csv("pages/data/Data_ready.csv")
dat['Date'] = pd.to_datetime(dat['Date'], format='mixed', utc=True)
dat.sort_values(by="Date", inplace=True)
for i in range(len(dat)):
    dat.loc[i,'Year']=datetime.date(dat.loc[i,'Date']).year

###################################### FILTRAGE ZA ###################################################
if len(Selection_ZA)==1:
    data = dat[dat[Selection_ZA[0]]==1]
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==2:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==3:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==4:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==5:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==6:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==7:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==8:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==9:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1],dat[dat[Selection_ZA[8]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_ZA)==10:
    data = pd.concat([dat[dat[Selection_ZA[0]]==1],dat[dat[Selection_ZA[1]]==1],dat[dat[Selection_ZA[2]]==1],dat[dat[Selection_ZA[3]]==1],dat[dat[Selection_ZA[4]]==1],dat[dat[Selection_ZA[5]]==1],dat[dat[Selection_ZA[6]]==1],dat[dat[Selection_ZA[7]]==1],dat[dat[Selection_ZA[8]]==1],dat[dat[Selection_ZA[9]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
else:
    data = dat.copy()
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
#######################################################################################################

data_bis =data.copy()
data_bis['Date'] = pd.to_datetime(data_bis['Date'], format='mixed', utc=True)
data_bis.set_index('Date', inplace=True)

data_resampled =data_bis.resample(rule="3D").size()
liste_dates = data_resampled.index.values
liste_comptes = data_resampled.values

df = pd.DataFrame([liste_dates,liste_comptes], index=['Date','Compte_mensuel']).T
df['Date'] = pd.to_datetime(df['Date'], format='mixed', utc=True)
for i in range(len(df)):
    df.loc[i,'Year']=datetime.date(df.loc[i,'Date']).year

start_date_year = data['Year'].iloc[0]-1
end_date_year = data['Year'].iloc[-1]
data_maps = data.copy()

###################################### VISUALISATION #################################################
st.subheader('Evolution temporelle')
with st.container(border=True):
    row1 = st.columns(2)

    with row1[0]:
        selection_dates = st.slider(':red[Zoomer sur une période plus récente]',min_value=start_date_year,max_value=end_date_year)
        nb_enregistrements = len(data[data.Year >= selection_dates])
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=data['Date'][data.Year >= selection_dates], 
            y=data['Compte_cumulé'][data.Year >= selection_dates],
            mode='lines+markers'))
        fig1.update_layout(
            title='Cumul dans le temps des enregistrements',
            xaxis_title='Date',
            yaxis_title='Compte cumulé',
            width=500,
            height=400)
        st.plotly_chart(fig1)
    
    with row1[1]:
        wch_colour_box = (250,120,120)
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

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df['Date'][df.Year >= selection_dates],
            y=df['Compte_mensuel'][df.Year >= selection_dates]
        ))
        fig2.update_layout(
            title='Cumul hebdomadaire des enregistrements',
            xaxis_title='Date',
            yaxis_title='Compte',
            width=500,
            height=400)
        st.plotly_chart(fig2)
        #st.bar_chart(data=df[df.Year >= selection_dates], x='Date', y='Compte_mensuel',height=300)

st.subheader('Evolution spatiale')
with st.container(border=True):
    row2 = st.columns(2)

    with row2[0]:
        nb_enregistrements_avec_localisation = len(dat)
        wch_colour_box = (250,120,120)
        wch_colour_font = (250,250,250)
        fontsize = 25
        valign = "right"
        iconname = "fas fa-asterisk"
        sline = nb_enregistrements_avec_localisation
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
        i = "Nb d'enregistrements localisés"

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
        st.map(dat[dat.Year >= selection_dates],latitude='lat',longitude='long',zoom=1)
    with row2[1]:
        nb_enregistrements_avec_localisation = len(data)
        zoom_france = 3
        zoom_monde = 1
        if len(Selection_ZA)>0:
            zoom = zoom_france
            wch_colour_box = (250,120,120)
            wch_colour_font = (250,250,250)
            fontsize = 15
            valign = "right"
            iconname = "fas fa-asterisk"
            sline = nb_enregistrements_avec_localisation
            lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
            i = Selection_ZA_str

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

            st.map(data[data.Year >= selection_dates][data['lat']>45],latitude='lat',longitude='long',zoom=zoom)
        else:
            zoom = zoom_monde



with st.container(border=True):
    row3 = st.columns(2)

    with row3[0]:

        data_format = data['format']
        cnt = data_format.value_counts()[0:9]
        somme_formats_vis = cnt.values.sum()
        
        colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen','cyan','rose','violet','green','red']

        fig3 = go.Figure()
        fig3.add_trace(go.Pie(labels=cnt.index.values, values=cnt.values))
        fig3.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig3.update_layout(
            title='Formats publiés',
            xaxis_title='Compte',
            yaxis_title='Formats',
            width=500,
            height=500)
        st.plotly_chart(fig3)
        st.markdown(f'Pour {somme_formats_vis} Enregistrements/{nb_enregistrements}')

    with row3[1]:

        data_orga = data['Org']
        cnt_orga = data_orga.value_counts()[0:10]
        somme_orga_vis = cnt_orga.values.sum()
        
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            y=cnt_orga.index.values,
            x=cnt_orga.values,
            orientation='h'
        ))
        fig4.update_layout(
            title='Organisations publiantes',
            xaxis_title='Compte',
            width=500,
            height=500)
        st.plotly_chart(fig4)
        st.markdown(f'Pour {somme_orga_vis} enregistrements/{nb_enregistrements}')

with st.container(border=True):

    fig5 = go.Figure()
    if len(Selection_ZA)!=0:
        for za in Selection_ZA:
            fig5.add_trace(go.Box(
                y=data['tagNumber'][data[za]==1],
                name=za
            ))
    else:
        fig5.add_trace(go.Box(
                y=data['tagNumber'],
                name='Tout les enregistrements'
            ))
    fig5.update_layout(
            title='Nombre de mots clés',
            yaxis_title='Nombre',
            width=500,
            height=500)
    st.plotly_chart(fig5)
    

    liste_tagNumber = []
    for i,x in enumerate(data.columns):
        if 'Number' in data.columns[i]:
            liste_tagNumber.append(x)
    liste_tagNumber.remove('tagNumber')

    data_numbers = data[liste_tagNumber]
    listes_to_drop = []
    for i,x in enumerate(liste_tagNumber):
        c=0
        for j,u in enumerate(data_numbers.index):
            try:
                if data_numbers.loc[u,x]=='-':
                    c += 1
            except:
                pass
        if (c/(len(data_numbers)))>0.9:
            listes_to_drop.append(x)
    data_numbers.drop(columns=listes_to_drop, inplace=True)
    liste_columns = []
    for k in range(len(data_numbers.columns)):
        liste_columns.append(data_numbers.columns[k].replace('Number', ''))

    fig6 = go.Figure()
    fig6.add_trace(go.Heatmap(
        x=liste_columns,
        z=data_numbers
    ))
    fig6.update_layout(
            title='Catégories des mots clés',
            width=1000,
            height=1000)
    st.plotly_chart(fig6)