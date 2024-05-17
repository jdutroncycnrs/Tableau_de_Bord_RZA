import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
import plotly.express as px
import plotly.graph_objects as go
import time
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

title = "Analyse des catalogues de cat.InDoRes"
s_title = f"<p style='font-size:50px;color:rgb(140,140,140)'>{title}</p>"
st.markdown(s_title,unsafe_allow_html=True)

liste_ZAs= ['ZAA','ZAAJ','ZAAR','ZAEU','ZABR','ZABRI','ZAM','ZAL','ZAS','ZAPygar']
liste_OHMs =['OHM_BMProvence','OHMI_Tessekere','OHM_Pyrenees','OHM_VRhone','OHMI_Pima','OHMI_Estarreja','OHM_Mediterraneen','OHM_Oyapock','OHMI_Nunavik','OHM_Caraibes','OHM_PDBitche','OHMI_Patagonia','OHM_Fessenheim']

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

if len(Selection_ZA)>0:
    Selection_ZA_str = Selection_ZA[0]
    for i in range(1,len(Selection_ZA)):
        Selection_ZA_str+="+" + Selection_ZA[i]

if len(Selection_OHM)>0:
    Selection_OHM_str = Selection_OHM[0]
    for i in range(1,len(Selection_OHM)):
        Selection_OHM_str+="+" + Selection_OHM[i]

###################################### LECTURE DATA NETTOYEES #########################################
fichier= 'Enregistrements_RZA_150524_ready'
dat = pd.read_csv(f"pages/data/{fichier}.csv")
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
elif len(Selection_OHM)==1:
    data = dat[dat[Selection_OHM[0]]==1]
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==2:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==3:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==4:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==5:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==6:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1],dat[dat[Selection_OHM[5]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==7:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1],dat[dat[Selection_OHM[5]]==1],dat[dat[Selection_OHM[6]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==8:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1],dat[dat[Selection_OHM[5]]==1],dat[dat[Selection_OHM[6]]==1],dat[dat[Selection_OHM[7]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==9:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1],dat[dat[Selection_OHM[5]]==1],dat[dat[Selection_OHM[6]]==1],dat[dat[Selection_OHM[7]]==1],dat[dat[Selection_OHM[8]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
elif len(Selection_OHM)==10:
    data = pd.concat([dat[dat[Selection_OHM[0]]==1],dat[dat[Selection_OHM[1]]==1],dat[dat[Selection_OHM[2]]==1],dat[dat[Selection_OHM[3]]==1],dat[dat[Selection_OHM[4]]==1],dat[dat[Selection_OHM[5]]==1],dat[dat[Selection_OHM[6]]==1],dat[dat[Selection_OHM[7]]==1],dat[dat[Selection_OHM[8]]==1],dat[dat[Selection_OHM[9]]==1]],axis=0)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
else:
    data = dat.copy()
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', utc=True)
    data.sort_values(by="Date", inplace=True)
    data.loc[:,'Compte_cumulé']=np.arange(len(data))+1
#######################################################################################################

piq_one_check = st.sidebar.checkbox("Selection d'un enregistrement unique")

date_fichier = st.sidebar.markdown(f'Le fichier utilisé : {fichier}')



###################################### VISUALISATION #################################################

if piq_one_check==True:
    if 'count' not in st.session_state:
        st.session_state.count = 0
    def increment_counter():
        st.session_state.count += 1
    def reset_counter():
        st.session_state.count = 0

    col01,col02,col03 = st.columns([0.8,0.1,0.1])
    with col01:
        piq_one = st.selectbox(label='',options=data['resourceTitleObject.default'], index=st.session_state.count)
    with col02:
        st.markdown('')
        st.markdown('')
        st.button(':heavy_plus_sign:',on_click=increment_counter)
    with col03:
        st.markdown('')
        st.markdown('')
        st.button('reset',on_click=reset_counter)

    data = data[data['resourceTitleObject.default']==piq_one]
    data['new_index']=np.arange(0,len(data))
    data.set_index('new_index', inplace=True)
    
    #st.metric(label='Auteur(e)',value=str(data.loc[0,'contact']))

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label='Date', value=str(data.loc[0,'Date']))
        st.metric(label='Format', value=str(data.loc[0,'format']))
        st.metric(label='Organisation', value=str(data.loc[0,'Org']))
        st.metric(label="Contrainte d'accès", value=str(data.loc[0,'cl_accessConstraints.default']))
        st.metric(label='Thématique générale', value=str(data.loc[0,'cl_topic.default']))

    with col2:
        st.metric(label='Identifiant', value=str(data.loc[0,'uuid']))
        st.metric(label='Status', value=str(data.loc[0,'cl_status.default']))
        st.metric(label='Distributeur', value=str(data.loc[0,'groupPublished']))
        st.metric(label="Contrainte d'usage", value=str(data.loc[0,'cl_useConstraints.default']))
        st.metric(label='Popularité', value=str(data.loc[0,'popularity']))

    if data.loc[0,'lat']==0:
        pass
    else:
        st.map(data,latitude='lat',longitude='long',zoom=8,color='#FEBB5F')
      
    data_to_show = data.copy()
    data_to_show.drop(columns=['cl_topic.default','cl_status.default','cl_hierarchyLevel.default','cl_accessConstraints.default','cl_useConstraints.default','resourceTitleObject.default','Date','groupPublished','Compte_cumulé','Year','long','lat','popularity','Unnamed: 0','location','Org','format','uuid','recordOwner'], inplace=True)
    l_to_supp = []
    for i,x in enumerate(data_to_show.columns):
        if data_to_show.loc[0,x]=='-':
            l_to_supp.append(x)

    data_to_show.drop(columns=l_to_supp,inplace=True)
    liste_tagNumber_bis = []
    for i,x in enumerate(data_to_show.columns):
        if 'Number' in data_to_show.columns[i]:
            liste_tagNumber_bis.append(x)
    data_to_show.drop(columns=liste_tagNumber_bis, inplace=True)
    liste_ZAs_bis =liste_ZAs.copy()
    data_to_show.drop(columns=liste_ZAs_bis, inplace=True)
    try:
        data_to_show['mot_clés']=data_to_show.loc[0,data_to_show.columns[0]]
        try:
            for c in range(1,len(data_to_show.columns)):
                data_to_show['mot_clés'] +=',' + data_to_show.loc[0,data_to_show.columns[c]]
        except:
            pass

        l= re.split(',', data_to_show.loc[0,'mot_clés'])
        l2 = list(set(l))
        for i in range(len(l2)):
            st.metric(label=f'mot clé {i+1}', value=l2[i])
    except:
        pass

elif len(data)!=0:

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

    st1 = 'Evolution temporelle'
    s_st1 = f"<p style='font-size:30px;color:rgb(140,140,140)'>{st1}</p>"
    st.markdown(s_st1,unsafe_allow_html=True)
    with st.container(border=True):
        row1 = st.columns(2)

        with row1[0]:
            selection_dates = st.slider(':grey[Zoomer sur une période plus récente]',min_value=start_date_year,max_value=end_date_year)
            nb_enregistrements = len(data[data.Year >= selection_dates])
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=data['Date'][data.Year >= selection_dates], 
                y=data['Compte_cumulé'][data.Year >= selection_dates],
                mode='lines+markers',
                line=dict(color='#ebbe31', width=1),
                marker=dict(color='white',size=0.2)))
            fig1.update_layout(
                title='Cumul dans le temps des enregistrements',
                xaxis_title='Date',
                yaxis_title='Compte cumulé',
                width=500,
                height=400)
            st.plotly_chart(fig1)
        
        with row1[1]:
            wch_colour_box = (250,250,220)
            wch_colour_font = (90,90,90)
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
            fig2.update_traces(marker_color='#FEBB5F', marker_line_color='#FEBB5F',
                  marker_line_width=3)
            fig2.update_layout(
                title='Cumul hebdomadaire des enregistrements',
                xaxis_title='Date',
                yaxis_title='Compte',
                width=500,
                height=400)
            st.plotly_chart(fig2)

    st2 = 'Evolution spatiale'
    s_st2 = f"<p style='font-size:30px;color:rgb(140,140,140)'>{st2}</p>"
    st.markdown(s_st2,unsafe_allow_html=True)
    with st.container(border=True):
        row2 = st.columns(2)

        with row2[0]:
            nb_enregistrements_avec_localisation = len(dat)
            wch_colour_box = (250,250,220)
            wch_colour_font = (90,90,90)
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
            st.map(dat[dat.Year >= selection_dates],latitude='lat',longitude='long',zoom=1,color='#FEBB5F')
        with row2[1]:
            nb_enregistrements_avec_localisation = len(data[data.Year >= selection_dates])
            data_mappees = data[data['lat']>40]
            zoom_france = 3
            zoom_monde = 1
            if len(Selection_ZA)>0:
                zoom = zoom_france
                wch_colour_box = (250,250,220)
                wch_colour_font = (90,90,90)
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
                st.map(data_mappees[data_mappees.Year >= selection_dates],latitude='lat',longitude='long',zoom=zoom,color='#FEBB5F')

            elif len(Selection_OHM)>0:
                zoom = zoom_france
                wch_colour_box = (250,250,100)
                wch_colour_font = (90,90,90)
                fontsize = 15
                valign = "right"
                iconname = "fas fa-asterisk"
                sline = nb_enregistrements_avec_localisation
                lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
                i = Selection_OHM_str

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
                st.map(data_mappees[data_mappees.Year >= selection_dates],latitude='lat',longitude='long',zoom=zoom,color='#FEBB5F')
            else:
                pass



    with st.container(border=True):
        row3 = st.columns(2)

        with row3[0]:

            data_format = data['format'][data.Year >= selection_dates]
            cnt = data_format.value_counts()[0:6]
            somme_formats_vis = cnt.values.sum()
            
            colors = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0']

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

            data_orga = data['Org'][data.Year >= selection_dates]
            cnt_orga = data_orga.value_counts()[0:10]
            somme_orga_vis = cnt_orga.values.sum()
            
            fig4 = go.Figure()
            for i in range(10):
                cnt_orga_ = data_orga.value_counts()[i:i+1]
                fig4.add_trace(go.Bar(
                        y=cnt_orga_.index.values,
                        x=cnt_orga_.values,
                        orientation='h',
                        showlegend=False,
                        marker=dict(color=colors[i])
                        ))
            fig4.update_layout(
                title='Organisations publiantes',
                xaxis_title='Compte',
                width=500,
                height=500)
            st.plotly_chart(fig4)
            st.markdown(f'Pour {somme_orga_vis} enregistrements/{nb_enregistrements}')

    with st.container(border=True):
        row4 = st.columns([0.7,0.3])
        with row4[0]:
            data_useC = data['cl_useConstraints.default'][data.Year >= selection_dates]
            cnt_useC = data_useC.value_counts()
            fig = go.Figure()
            fig.add_trace(go.Pie(labels=cnt_useC.index.values, values=cnt_useC.values))
            fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                        marker=dict(colors=colors, line=dict(color='#000000', width=2)))
            fig.update_layout(
                    title="Contraintes d'usage",
                    width=500,
                    height=500)
            st.plotly_chart(fig, use_container_width=True)

        with row4[1]:
            data_status = data['cl_status.default'][data.Year >= selection_dates]
            cnt_status = data_status.value_counts()
            cnt_status_df = pd.DataFrame(cnt_status)
            fig_ = go.Figure()
            fig_.add_trace(go.Table(cells=dict(values=[cnt_status_df.index.values ,cnt_status_df.values],
                                               #fill_color='lightgrey',
                                               line_color='#FEBB5F')))
            fig_.update_layout(
                    title="Status",
                    width=300,
                    height=500)
            st.plotly_chart(fig_)

    with st.container(border=True):
        data_topics = data[['Date','cl_topic.default']][data.Year >= selection_dates]
        data_topics['new_index']=np.arange(0,len(data_topics))
        data_topics.set_index('new_index', inplace=True)
        liste_topics = []
        for i in range(len(data_topics)):
            lti = re.split(',',data_topics.loc[i,'cl_topic.default'])
            for j in lti:
                liste_topics.append(j.strip().lower() )

        liste_topics_ =list(set(liste_topics))
        dico_topics = {}
        for top in liste_topics:
            dico_topics[top]=liste_topics.count(top)
                
        df_topics = pd.DataFrame(list(dico_topics.items()),columns=['topics','compte'])
        df_topics_ = df_topics.T

        fig9 = go.Figure()
        fig9.add_trace(go.Heatmap(
            x=df_topics_.loc['topics', :].values,
            z=df_topics_,
            colorscale='solar',
            text=df_topics_,
            texttemplate="%{text}",
            textfont={"size":10}))
        fig9.update_yaxes(visible=False,range=[0.9, 1.1])
        fig9.update_xaxes(tickangle=45)
        fig9.update_layout(
            title='Occurence des Thématiques',
                width=1000,
                height=500)
        st.plotly_chart(fig9,use_container_width=True)

    with st.container(border=True):
        data_pop = data.copy()
        data_pop_ = data_pop[data_pop.Year >= selection_dates]
        m = max(data_pop_['popularity'])
        fig5 = go.Figure()
        if len(Selection_ZA)!=0:
            for i,za in enumerate(Selection_ZA):
                fig5.add_trace(go.Histogram(
                    x=data_pop_['popularity'][data_pop_[za]==1],
                    name=za,
                    xbins=dict(
                        start=-0.0,
                        end=80.0,
                        size=0.5),
                    marker_color=colors[i]
        ))
        elif len(Selection_OHM)!=0:
            for i, ohm in enumerate(Selection_OHM):
                fig5.add_trace(go.Histogram(
                    x=data_pop_['popularity'][data_pop_[ohm]==1],
                    name=ohm,
                    xbins=dict(
                        start=-0.0,
                        end=80.0,
                        size=0.5),
                    marker_color=colors[i]
        ))
        else:
            fig5.add_trace(go.Histogram(
                    x=data_pop_['popularity'],
                    name='Tout les enregistrements',
                    xbins=dict(
                        start=-0.0,
                        end=80.0,
                        size=0.5),
                    marker_color='#FEBB5F'))
        fig5.update_layout(
                title='Popularité des enregistrements',
                yaxis_title='Nombre',
                width=1000,
                height=500)
        st.plotly_chart(fig5)
        st.markdown(f"La popularité la plus élevée = {m}" )


    with st.container(border=True):
        data_tagNumber = data.copy()
        data_tagNumber_ = data_tagNumber[data_tagNumber.Year >= selection_dates]
        fig6 = go.Figure()
        if len(Selection_ZA)!=0:
            for i, za in enumerate(Selection_ZA):
                fig6.add_trace(go.Box(
                    y=data_tagNumber_['tagNumber'][data_tagNumber_[za]==1],
                    name=za,
                    marker_color=colors[i]
                ))
        elif len(Selection_OHM)!=0:
            for i, ohm in enumerate(Selection_OHM):
                fig6.add_trace(go.Box(
                    y=data_tagNumber_['tagNumber'][data_tagNumber_[ohm]==1],
                    name=ohm,
                    marker_color=colors[i]
                ))
        else:
            fig6.add_trace(go.Box(
                    y=data_tagNumber_['tagNumber'],
                    name='Tout les enregistrements',
                    marker_color='#FEBB5F'
                ))
        fig6.update_layout(
                title='Nombre de mots clés',
                yaxis_title='Nombre',
                width=1000,
                height=500)
        st.plotly_chart(fig6)
        

        liste_tagNumber = []
        for i,x in enumerate(data.columns):
            if 'Number' in data.columns[i]:
                liste_tagNumber.append(x)
        #liste_tagNumber.remove('tagNumber')

        data_numbers = data[liste_tagNumber][data.Year >= selection_dates]
        data_numbers.drop(columns=['tagNumber'],inplace=True)
        listes_to_drop = []
        for i,x in enumerate(liste_tagNumber):
            c=0
            for j,u in enumerate(data_numbers.index):
                try:
                    if data_numbers.loc[u,x]>str(15):
                        data_numbers.loc[u,x]='-'
                    if data_numbers.loc[u,x]=='-':
                        c += 1
                except:
                    pass
            if (c/(len(data_numbers)))>0.99:
                listes_to_drop.append(x)
        data_numbers.drop(columns=listes_to_drop, inplace=True)
        liste_columns = []
        for k in range(len(data_numbers.columns)):
            liste_columns.append(data_numbers.columns[k].replace('Number', ''))

        if len(data_numbers)<50:
            fig7 = go.Figure()
            fig7.add_trace(go.Heatmap(
                x=liste_columns,
                z=data_numbers,
                colorscale = 'solar',
                #text=data_numbers,
                #texttemplate="%{text}",
                #textfont={"size":20}
            ))
            fig7.update_layout(
                    title='Catégories des mots clés',
                    width=1000,
                    height=500)
            st.plotly_chart(fig7)

        elif len(data_numbers)<750:
            fig7 = go.Figure()
            fig7.add_trace(go.Heatmap(
                x=liste_columns,
                z=data_numbers,
                colorscale = 'solar'
                #text=data_numbers,
                #texttemplate="%{text}",
                #textfont={"size":10}
            ))
            fig7.update_layout(
                    title='Catégories des mots clés',
                    width=1000,
                    height=700)
            st.plotly_chart(fig7)

        else:
            fig7 = go.Figure()
            fig7.add_trace(go.Heatmap(
                x=liste_columns,
                z=data_numbers,
                colorscale = 'solar'
                #text=data_numbers,
                #texttemplate="%{text}",
                #textfont={"size":10}
            ))
            fig7.update_layout(
                    title='Catégories des mots clés',
                    width=1000,
                    height=1000)
            st.plotly_chart(fig7)

        st.markdown('Matrice filtrée à 15 mots clés maxi (et 1% des cas (outliers) sont absents)')

    ########### MOTS CLES #################

    data_mots_cles = data[['Date','mot_clés']][data.Year >= selection_dates]
    data_mots_cles['new_index']=np.arange(0,len(data_mots_cles))
    data_mots_cles.set_index('new_index', inplace=True)
    liste_mots_cles_generale = []
    for i in range(len(data_mots_cles)):
        li = re.split(',',data_mots_cles.loc[i,'mot_clés'])
        for lii in li:
            if lii != '-':
                liste_mots_cles_generale.append(lii.strip().lower())
        
    liste_mots_cles_generale_ = list(set(liste_mots_cles_generale))
    
    st.metric(label='Nombre de mots clés dans la sélection filtrée :', value=len(liste_mots_cles_generale))
    st.metric(label='Nombre de mots clés différents dans la sélection filtrée :', value=len(liste_mots_cles_generale_))


    if st.button('Cliquez pour voir les mots les plus utilisés'):
        with st.spinner('On vous concocte ça rapidement...'):

            dico = {}
            for mot in liste_mots_cles_generale:
                dico[mot]=liste_mots_cles_generale.count(mot)
            
            df_mots_cles = pd.DataFrame(list(dico.items()),columns=['mot clé','compte'])
            df_mots_cles.sort_values(by='compte',ascending=False, inplace=True)

            fig8 = go.Figure()
            fig8.add_trace(go.Bar( 
                x=df_mots_cles['mot clé'].head(20),
                y=df_mots_cles['compte'].head(20)))
            fig8.update_traces(marker_color='#FEBB5F', marker_line_color='#FEBB5F',
                  marker_line_width=3)
            fig8.update_layout(
                            title='Mots clés les plus fréquents',
                            width=1000,
                            height=500)
            st.plotly_chart(fig8)

############## TEST CONTACT ##############################################################################
#    data_contacts = data['contact'].unique()
#   st.table(data_contacts)

else:
    st.write("Il n'y a aucune donnée à visualiser")