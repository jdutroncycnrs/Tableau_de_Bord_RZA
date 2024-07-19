import streamlit as st
import pandas as pd
import datetime
import glob
import requests
import json
import re
from Recuperation_uuids import scraping_GN, uuids_cleaning, recup_group
from Traitement_records import transcript_json

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="Analyse des fiches de métadonnées du GeoNetwork",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

############ PARAMETRES ############################################

d = datetime.date.today()

url = "https://cat.indores.fr/geonetwork/srv/api/records/"

headers_json = {"accept":"application/json",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}

headers_xml = {"accept":"application/xml",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}

headers_text = {"accept":"text/plain",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}

couleur_subtitles = (250,100,0)
taille_subtitles = "25px"
couleur_subsubtitles = (150,0,150)
taille_subsubtitles = "25px"

############## RECUPERATION DES IDENTIFIANTS EXISTANTS #########################

fi = glob.glob(f"pages/data/uuids/uuid_cat_InDoRes_clean*.csv")

if len(fi)!=0:
    fichier_uuids = fi[-1]
    derniere_date_recup = f"Dernière date de récupération des identifiants: {fichier_uuids[40:-4]}"
    s_derniere_date_recup  = f"<p style='font-size:25px;color:rgb(0,150,0)'>{derniere_date_recup}</p>"
    st.markdown(s_derniere_date_recup ,unsafe_allow_html=True)
    uuids = pd.read_csv(fichier_uuids, index_col=[0])
else:
    st.write('Il est nécessaire de mettre à jour la récupération des uuids')

########### RECUPERATION DES IDENTIFIANTS VIA BOUTON ############################

RecupIdentifiants = st.sidebar.button("Récupération des identifiants")
if RecupIdentifiants:
    with st.spinner("Connexion au GeoNetwork et récupération des identifiants existants"):
        m = scraping_GN(d)   
        uuids_cleaning(d)
        st.experimental_rerun()

admin_pass = 'admin'
admin_action = st.sidebar.text_input(label="Pour l'administrateur")

if admin_action == admin_pass:
    Recup_groupes = st.sidebar.button('recup des groupes')
    if Recup_groupes:
        with st.spinner("La récup des groupes est en cours"):
            groupes = []
            liste_u = []
            for i in range(len(uuids)):
                u = uuids.loc[i,'uuid_cat_InDoRes']
                try:
                    g = recup_group(uuid=u)
                    groupes.append(g)
                    liste_u.append(u)
                except:
                    g = ""
                    groupes.append(g)
                    liste_u.append(u)

            df_group = pd.DataFrame({'Identifiant':liste_u, 'Groupe':groupes})
            df_group.to_csv("pages/data/infos_MD/infos_groupes.csv")


########## TITRE DE LA PAGE ############################################
title = "Visualisation des fiches GN"
s_title = f"<p style='font-size:50px;color:rgb(140,140,140)'>{title}</p>"
st.markdown(s_title,unsafe_allow_html=True)

if 'count' not in st.session_state:
    st.session_state.count = 0
def increment_counter():
    st.session_state.count += 1
def reset_counter():
    st.session_state.count = 0

with st.container(border=True):
    s1 = "IDENTIFIEUR"
    s_s1 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s1}</p>"
    st.markdown(s_s1,unsafe_allow_html=True)

    col01,col02,col03 = st.columns([0.8,0.1,0.1])
    with col01:
        identifieur = st.selectbox(label='',options=uuids['uuid_cat_InDoRes'], index=st.session_state.count)
    with col02:
        st.markdown('')
        st.markdown('')
        button1 = st.button(':heavy_plus_sign:',on_click=increment_counter)
    with col03:
        st.markdown('')
        st.markdown('')
        button2 =st.button('R',on_click=reset_counter)

########## CONNEXION AU GEONETWORK ############################################

    try:
        df = pd.read_csv(f'pages/data/fiches_csv/{identifieur}.csv',index_col=[0])
    except:
        url_ = url + identifieur
        resp1 = requests.get(url_,headers=headers_json)
        if resp1.status_code == 200:
            resp_json=resp1.json()
            with open(f"pages/data/fiches_json/{identifieur}.json", "w") as f:
                json.dump(resp_json, f, indent=4)
     
        resp2 = requests.get(url_,headers=headers_xml)
        if resp2.status_code == 200:
            xml_content = resp2.text
            with open(f"pages/data/fiches_xml/{identifieur}.xml", 'w') as file:
                file.write(xml_content)

        url_asso = url + identifieur +"/associated?rows=100"
        resp_asso = requests.get(url_asso,headers=headers_json)
        if resp_asso.status_code == 200:
            resp_asso_json=resp_asso.json()
            with open(f"pages/data/associated_resources/resource_{identifieur}.json", "w") as f:
                json.dump(resp_asso_json, f, indent=4)

        url_attach = url + identifieur +"/attachments"
        resp_attach = requests.get(url_attach,headers=headers_json)
        if resp_attach.status_code == 200:
            resp_attach_json=resp_attach.json()
            with open(f"pages/data/attachments/attachments_{identifieur}.json", "w") as f:
                json.dump(resp_attach_json, f, indent=4)

    
    try:
        df_infos = pd.read_csv("pages/data/infos_MD/infos_groupes.csv",index_col=[0])
    except:
        df_infos = pd.DataFrame(columns=['Identifiant','Groupe'])
        df_infos.to_csv("pages/data/infos_MD/infos_groupes.csv")
    liste_id = list(df_infos.Identifiant)
    if identifieur in liste_id:
        pass
    else:
        try:
            g = recup_group(uuid=identifieur)
        except:
            g = ""
        d = pd.DataFrame(data = [[identifieur,g]],columns=['Identifiant','Groupe'])
        df_infos_ = pd.concat([df_infos,d], axis=0)
        df_infos = df_infos_
        df_infos.reset_index(inplace=True)
        df_infos.drop(columns='index',inplace=True)
        df_infos.to_csv("pages/data/infos_MD/infos_groupes.csv")
      

################ TRAITEMENT DU JSON #############################################################
    try:
        with open(f"pages/data/fiches_json/{identifieur}.json", 'r') as f:
            data = json.load(f)

        with open(f'pages/data/fiches_txt/{identifieur}.txt', 'w') as file:
            transcript_json(data, file)

        with open(f'pages/data/fiches_txt/{identifieur}.txt', 'r') as f:
            d = f.read()

        listi = re.split('µ',d)

        df = pd.DataFrame(listi, columns=['Results'])
        for u in range(len(df)):
            p = re.split('§',df.loc[u,'Results'])
            try:
                df.loc[u,'Valeurs']=p[1]
            except:
                pass
            try:
                df.loc[u,'Clés']=p[0].replace('.','£')
            except:
                pass

        for j in range(len(df)):
            pp = re.split('£',df.loc[j,'Clés'])
            for k in range(15):
                try:
                    df.loc[j,f'K{k}']=pp[k]
                except:
                    pass
        df.to_csv(f'pages/data/fiches_csv/{identifieur}.csv')
        visu = df[['Clés','Valeurs']]
        st.dataframe(visu, use_container_width=True)
    
    except:
        st.write("Le processus n'a pas fonctionné")
#########  VARIABLES ########################################################
try:
    Langue = df['Valeurs'][df['Clés']=="gmd:language£gco:CharacterString£#text:"].values[0]
except:
    Langue = ""
try:
    JeuDeCaracteres = df['Valeurs'][df['Clés']=="gmd:characterSet£gmd:MD_CharacterSetCode£@codeListValue:"].values[0]
except:
    JeuDeCaracteres =""
try:
    Type = df['Valeurs'][df['Clés']=="gmd:hierarchyLevel£gmd:MD_ScopeCode£@codeListValue:"].values[0]
except:
    Type =""
try:
    Date = df['Valeurs'][df['Clés']=="gmd:dateStamp£gco:DateTime£#text:"].values[0]
except:
    Date = ""
try:
    Standard = df['Valeurs'][df['Clés']=="gmd:metadataStandardName£gco:CharacterString£#text:"].values[0]
except:
    Standard = ""
try:
    Version_standard = df['Valeurs'][df['Clés']=="gmd:metadataStandardVersion£gco:CharacterString£#text:"].values[0]
except:
    Version_standard = ""
try:
    Nom_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values[0]
except:
    Nom_contact = ""
try:
    Organisation_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values[0]
except:
    Organisation_contact = ""
try:
    Position_contact =df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values[0]
except:
    Position_contact = ""
try:
    Tel_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values[0]
except:
    Tel_contact = ""

try:
    SystemReference =  df['Valeurs'][df['Clés']=="gmd:referenceSystemInfo£gmd:MD_ReferenceSystem£gmd:referenceSystemIdentifier£gmd:RS_Identifier£gmd:code£gco:CharacterString£#text:"].values
except:
    SystemReference = ""

try: 
    Titre = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:title£gco:CharacterString£#text:"].values[0]
except:
    Titre = ""
try:
    Abstract =df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:abstract£gco:CharacterString£#text:"].values[0]
except:
    Abstract = ""
try:
    Date_creation = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:date£gco:DateTime£#text:"].values[0]
except:
    Date_creation = ""
try:
    Purpose = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:purpose£gco:CharacterString£#text:"].values[0]
except:
    Purpose = ""
try:
    Status = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:status£gmd:MD_ProgressCode£@codeListValue:"].values[0]
except:
    Status = ""
try:
    Freq_maj = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceMaintenance£gmd:MD_MaintenanceInformation£gmd:maintenanceAndUpdateFrequency£gmd:MD_MaintenanceFrequencyCode£@codeListValue:"].values[0]
except:
    Freq_maj = ""

#try:
    #themes = []
    #cpt_th = 0
    #cpt_mots = 0
    #for l in range(len(df)):
    #    if df.loc[l,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:type£gmd:MD_KeywordTypeCode£@codeListValue:":
    #        themes.append([cpt_th,df.loc[l,'Valeurs']])
    #        cpt_th +=1
     #       cpt_mots = 0
     #   if df.loc[l,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:keyword£gco:CharacterString£#text:":
     #      cpt_mots += 1
#except:
    #themes = ""

######### VISUALISATION #######################################################

with st.container(border=True):
    s2 = "METADONNEES"
    s_s2 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s2}</p>"
    st.markdown(s_s2,unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        s2a = 'Date'
        s_s2a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2a}</p>"
        st.markdown(s_s2a,unsafe_allow_html=True)
        st.markdown(Date)
    with col2:
        s2b = 'Langue'
        s_s2b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2b}</p>"
        st.markdown(s_s2b,unsafe_allow_html=True)
        st.markdown(Langue)
    with col3:
        s2c = 'Jeu de caractères'
        s_s2c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2c}</p>"
        st.markdown(s_s2c,unsafe_allow_html=True)
        st.markdown(JeuDeCaracteres)
    with col4:
        s2d = 'Type'
        s_s2d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2d}</p>"
        st.markdown(s_s2d,unsafe_allow_html=True)
        st.markdown(Type)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        s2e = 'Nom du contact'
        s_s2e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2e}</p>"
        st.markdown(s_s2e,unsafe_allow_html=True)
        st.markdown(Nom_contact)
    with col2:
        s2f = 'Position du contact'
        s_s2f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2f}</p>"
        st.markdown(s_s2f,unsafe_allow_html=True)
        st.markdown(Position_contact)
    with col3:
        s2g = 'Orga du contact'
        s_s2g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2g}</p>"
        st.markdown(s_s2g,unsafe_allow_html=True)
        st.markdown(Organisation_contact)
    with col4:
        s2h = 'Tel du contact'
        s_s2h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2h}</p>"
        st.markdown(s_s2h,unsafe_allow_html=True)
        st.markdown(Tel_contact)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        s2i = 'Nom du standard'
        s_s2i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2i}</p>"
        st.markdown(s_s2i,unsafe_allow_html=True)
        st.markdown(Standard)
    with col2:
        s2j = 'Version du standard'
        s_s2j = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2j}</p>"
        st.markdown(s_s2j,unsafe_allow_html=True)
        st.markdown(Version_standard)
    with col3:
        pass
    with col4:
        pass

with st.container(border=True):
    s3 = "SYSTEME DE REFERENCE"
    s_s3 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s3}</p>"
    st.markdown(s_s3,unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        s3a = 'Systèmes renseignés'
        s_s3a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3a}</p>"
        st.markdown(s_s3a,unsafe_allow_html=True)
        for x in range(len(SystemReference)):
            st.markdown(SystemReference[x])
    with col2:
        pass
    with col3:
        pass
    with col4:
        pass

with st.container(border=True):
    s4 = "IDENTIFICATION"
    s_s4 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s4}</p>"
    st.markdown(s_s4,unsafe_allow_html=True)

    s4a = 'Titre'
    s_s4a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4a}</p>"
    st.markdown(s_s4a,unsafe_allow_html=True)
    st.markdown(Titre)

    s4b = 'Résumé'
    s_s4b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4b}</p>"
    st.markdown(s_s4b,unsafe_allow_html=True)
    st.markdown(Abstract)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        s4c = 'Date (création)'
        s_s4c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4c}</p>"
        st.markdown(s_s4c,unsafe_allow_html=True)
        st.markdown(Date_creation)
    with col2:
        s4d = 'Purpose'
        s_s4d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4d}</p>"
        st.markdown(s_s4d,unsafe_allow_html=True)
        st.markdown(Purpose)
    with col3:
        s4e = 'Status'
        s_s4e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4e}</p>"
        st.markdown(s_s4e,unsafe_allow_html=True)
        st.markdown(Status)
    with col4:
        s4f = 'Fréquence de maj'
        s_s4f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4f}</p>"
        st.markdown(s_s4f,unsafe_allow_html=True)
        st.markdown(Freq_maj)

with st.container(border=True):
    s5 = "MOTS CLES"
    s_s5 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s5}</p>"
    st.markdown(s_s5,unsafe_allow_html=True)


    #col1,col2,col3,col4 = st.columns(4)
    #for t in range(len(themes)):
    #    if len(themes[t])==2:
    #        if themes[t][0]==0:
     #           theme1 = themes[t][1]
      #      elif themes[t][0]==1:
      #          theme2 = themes[t][1]
      #      elif themes[t][0]==2:
       #         theme3 = themes[t][1]
    #with col1:
    #    s5a = theme1
    #    s_s5a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5a}</p>"
    #    st.markdown(s_s5a,unsafe_allow_html=True)
   # with col2:
    #    s5b = theme2
    #    s_s5b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5b}</p>"
    #    st.markdown(s_s5b,unsafe_allow_html=True)
    #with col3:
    #    s5c = theme3
    #    s_s5c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5c}</p>"
     #   st.markdown(s_s5c,unsafe_allow_html=True)
    #with col4:
   #    pass