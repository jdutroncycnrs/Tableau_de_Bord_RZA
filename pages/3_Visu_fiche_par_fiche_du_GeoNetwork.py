import streamlit as st
import pandas as pd
import datetime
import glob
import requests
import json
import re
import numpy as np
import plotly.express as px
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

########## VISUALISATION DU GROUPE ############################################

    group_ = pd.read_csv("pages/data/infos_MD/infos_groupes.csv", index_col=[0])
    #group_['Groupe'].fillna('Aucun groupe', inplace=True)
    #group_.to_csv("pages/data/infos_MD/infos_groupes.csv")

    wch_colour_box = (250,250,220)
    wch_colour_font = (90,90,90)
    fontsize = 25
    valign = "right"
    sline = group_['Groupe'][group_.Identifiant==identifieur].values[0]
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    #i = "Groupe associé à la fiche"

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
                                    </style><BR><span style='font-size: 25px; 
                                    margin-top: 0;'>{sline}</style></span></p>"""
    st.sidebar.markdown(lnk + htmlstr, unsafe_allow_html=True)


########### RECUPERATION DES IDENTIFIANTS VIA BOUTON ############################

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

        RecupIdentifiants = st.sidebar.button("Récupération des identifiants")
        if RecupIdentifiants:
            with st.spinner("Connexion au GeoNetwork et récupération des identifiants existants"):
                m = scraping_GN(d)   
                uuids_cleaning(d)
                st.experimental_rerun()

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
        #st.dataframe(visu, use_container_width=True)
    
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
    Nom_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values
except:
    try:
        Nom_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values
    except:
        Nom_contact = ""
try:
    Organisation_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values
except:
    try:
        Organisation_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values
    except:
        Organisation_contact = ""
try:
    Position_contact =df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values
except:
    try:
        Position_contact =df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values
    except:
        Position_contact = ""
try:
    Tel_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values
except:
    try:
        Tel_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values
    except:
        Tel_contact = ""
try:
    DeliveryPoint = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:deliveryPoint£gco:CharacterString£#text:"].values
except:
    try:
        DeliveryPoint = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:deliveryPoint£gco:CharacterString£#text:"].values
    except:
        DeliveryPoint = ""
try:
    CodePostal = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:postalCode£gco:CharacterString£#text:"].values
except:
    try:
        CodePostal = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:postalCode£gco:CharacterString£#text:"].values
    except:
        CodePostal = ""
try:
    Ville = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:city£gco:CharacterString£#text:"].values
except:
    try:
        Ville = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:city£gco:CharacterString£#text:"].values
    except:
        Ville = ""
try:
    Pays = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:country£gco:CharacterString£#text:"].values
except:
    try:
        Pays = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:country£gco:CharacterString£#text:"].values
    except:
        Pays =""
try:
    Email = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:electronicMailAddress£gco:CharacterString£#text:"].values[0]
except:
    Email = ""


try:
    SystemReference =  df['Valeurs'][df['Clés']=="gmd:referenceSystemInfo£gmd:MD_ReferenceSystem£gmd:referenceSystemIdentifier£gmd:RS_Identifier£gmd:code£gco:CharacterString£#text:"].values
except:
    SystemReference = ""
try:
    westBoundLongitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:westBoundLongitude£gco:Decimal£#text:"].values[0]
except:
    westBoundLongitude = ""
try:
    EastBoundLongitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:eastBoundLongitude£gco:Decimal£#text:"].values[0]
except:
    EastBoundLongitude = ""
try:
    SouthBoundLatitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:southBoundLatitude£gco:Decimal£#text:"].values[0]
except:
    SouthBoundLatitude = ""
try:
    NorthBoundLatitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:northBoundLatitude£gco:Decimal£#text:"].values[0]
except:
    NorthBoundLatitude = ""

try: 
    Titre = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:title£gco:CharacterString£#text:"].values[0]
except:
    Titre = ""
try: 
    FicheParent = df['Valeurs'][df['Clés']=="gmd:parentIdentifier£gco:CharacterString£#text:"].values[0]
except:
    FicheParent = ""
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

Type_dates = []
Dates = []
try:
    for li in range(len(df)):
        if df.loc[li,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:dateType£gmd:CI_DateTypeCode£@codeListValue:":
            Type_dates.append(df.loc[li,'Valeurs'])
except:
    pass
try:
    for l in range(len(df)):
        if df.loc[l,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:date£gco:Date£#text:":
            Dates.append(df.loc[l,'Valeurs'])
except:
    pass
liste_dates = []
try:
    for da in range(len(Type_dates)):
        liste_dates.append([Type_dates[da],Dates[da]])
except:
    pass

Liste_Theme = []
Liste_Thesaurus = []
Mots_cles = []
try:
    for u in range(len(df)):
        if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:type£gmd:MD_KeywordTypeCode£@codeListValue:":
            Liste_Theme.append([u,df.loc[u,'Valeurs']])
except:
    pass
try:
    for u in range(len(df)):
        if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:thesaurusName£gmd:CI_Citation£gmd:title£gco:CharacterString£#text:":
            Liste_Thesaurus.append([u,df.loc[u,'Valeurs']])
except:
    pass
try:
    for u in range(len(df)):
        if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:keyword£gco:CharacterString£#text:" or  df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:keyword£gmx:Anchor£#text:":
            Mots_cles.append([u,df.loc[u,'Valeurs']])
except:
    pass

theme_thesaurus_motsCles = []
mm = 0    
for th in range(1):
    liste_mots_cles = []
    try:
        if Liste_Theme[th][0]< Liste_Thesaurus[th][0]:
            for m in range(mm,len(Mots_cles)):
                if Mots_cles[m][0]<Liste_Theme[th][0]:
                    liste_mots_cles.append(Mots_cles[m][1])
                    mm = m
            theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],Liste_Thesaurus[th][1]])
    except:
        try:
            for m in range(mm,len(Mots_cles)):
                if Mots_cles[m][0]<Liste_Theme[th][0]:
                    liste_mots_cles.append(Mots_cles[m][1])
                    mm = m
            theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],"Aucun thésaurus"])
        except:
            theme_thesaurus_motsCles.append([liste_mots_cles,"Aucun thème","Aucun thésaurus"])

for th in range(1,len(Liste_Theme)):
    liste_mots_cles = []
    try:
        if Liste_Theme[th][0]< Liste_Thesaurus[th][0]:
            for m in range(mm+1,len(Mots_cles)):
                if Mots_cles[m][0]<Liste_Theme[th][0]:
                    liste_mots_cles.append(Mots_cles[m][1])
                    mm = m
            theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],Liste_Thesaurus[th][1]])
    except:
        try:
            for m in range(mm+1,len(Mots_cles)):
                if Mots_cles[m][0]<Liste_Theme[th][0]:
                    liste_mots_cles.append(Mots_cles[m][1])
                    mm = m
            theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],"Aucun thésaurus"])
        except:
            theme_thesaurus_motsCles.append([liste_mots_cles,"Aucun thème","Aucun thésaurus"])

try:
    UseLimitation = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:useLimitation£gco:CharacterString£#text:"].values[0]
except:
    UseLimitation =""
try:
    UseContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:useConstraints£gmd:MD_RestrictionCode£@codeListValue:"].values[0]
except:
    UseContrainte =""
try:
    AccesContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:accessConstraints£gmd:MD_RestrictionCode£@codeListValue:"].values[0]
except:
    AccesContrainte =""
try:
    AutreContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:otherConstraints£gco:CharacterString£#text:"].values[0]
except:
    AutreContrainte =""

try:
    Format = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:distributionFormat£gmd:MD_Format£gmd:name£gco:CharacterString£#text:"].values
except:
    Format = ""
try:
    Online_links = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:linkage£gmd:URL:"].values
except:
    Online_links = ""
try:
    Online_protocols = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:protocol£gco:CharacterString£#text:"].values
except:
    Online_protocols = ""
try:
    Online_nom = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:name£gco:CharacterString£#text:"].values
except:
    Online_nom = ""
try:
    Online_description = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:description£gco:CharacterString£#text:"].values
except:
    Online_description = ""

try:
    Niveau = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:scope£gmd:DQ_Scope£gmd:level£gmd:MD_ScopeCode£@codeListValue:"].values[0]
except:
    Niveau = ""
try:
    Conformite = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:report£gmd:DQ_DomainConsistency£gmd:result£gmd:DQ_ConformanceResult£gmd:pass£gco:Boolean£#text:"].values[0]
except:
    Conformite = ""
try:
    Genealogie = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:lineage£gmd:LI_Lineage£gmd:statement£gco:CharacterString£#text:"].values[0]
except:
    Genealogie = ""

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
        for x in range(len(Nom_contact)):
            st.markdown(Nom_contact[x])
    with col2:
        s2f = 'Position du contact'
        s_s2f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2f}</p>"
        st.markdown(s_s2f,unsafe_allow_html=True)
        for x in range(len(Position_contact)):
            st.markdown(Position_contact[x])
    with col3:
        s2g = 'Orga du contact'
        s_s2g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2g}</p>"
        st.markdown(s_s2g,unsafe_allow_html=True)
        for x in range(len(Organisation_contact)):
            st.markdown(Organisation_contact[x])
    with col4:
        s2h = 'Tel du contact'
        s_s2h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2h}</p>"
        st.markdown(s_s2h,unsafe_allow_html=True)
        for x in range(len(Tel_contact)):
            st.markdown(Tel_contact[x])

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        s2i = 'Adresse'
        s_s2i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2i}</p>"
        st.markdown(s_s2i,unsafe_allow_html=True)
        for x in range(len(DeliveryPoint)):
            st.markdown(DeliveryPoint[x])
    with col2:
        s2j = 'Code Postal'
        s_s2j = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2j}</p>"
        st.markdown(s_s2j,unsafe_allow_html=True)
        for x in range(len(CodePostal)):
            st.markdown(CodePostal[x])
    with col3:
        s2k = 'Ville'
        s_s2k = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2k}</p>"
        st.markdown(s_s2k,unsafe_allow_html=True)
        for x in range(len(Ville)):
            st.markdown(Ville[x])
    with col4:
        s2l = 'Pays'
        s_s2l = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2l}</p>"
        st.markdown(s_s2l,unsafe_allow_html=True)
        for x in range(len(Pays)):
            st.markdown(Pays[x])

    col1,col2,col3 = st.columns([0.25,0.25,0.5])
    with col1:
        s2m = 'Nom du standard'
        s_s2m = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2m}</p>"
        st.markdown(s_s2m,unsafe_allow_html=True)
        st.markdown(Standard)
    with col2:
        s2n = 'Version du standard'
        s_s2n = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2n}</p>"
        st.markdown(s_s2n,unsafe_allow_html=True)
        st.markdown(Version_standard)
    with col3:
        s2o = 'Adresse email du contact'
        s_s2o = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2o}</p>"
        st.markdown(s_s2o,unsafe_allow_html=True)
        st.markdown(Email)

with st.container(border=True):
    s3 = "SYSTEME DE REFERENCE & LIMITES GEOGRAPHIQUES"
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

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        s3c = 'Longitude Ouest'
        s_s3c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3c}</p>"
        st.markdown(s_s3c,unsafe_allow_html=True)
        st.markdown(westBoundLongitude)
    with col2:
        s3d = 'Longitude Est'
        s_s3d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3d}</p>"
        st.markdown(s_s3d,unsafe_allow_html=True)
        st.markdown(EastBoundLongitude)
    with col3:
        s3e = 'Latitude Sud'
        s_s3e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3e}</p>"
        st.markdown(s_s3e,unsafe_allow_html=True)
        st.markdown(SouthBoundLatitude)
    with col4:
        s3f = 'Latitude Nord'
        s_s3f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3f}</p>"
        st.markdown(s_s3f,unsafe_allow_html=True)
        st.markdown(NorthBoundLatitude)

with st.container(border=True):
    s4 = "IDENTIFICATION"
    s_s4 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s4}</p>"
    st.markdown(s_s4,unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        s4a = 'Titre'
        s_s4a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4a}</p>"
        st.markdown(s_s4a,unsafe_allow_html=True)
        st.markdown(Titre)
    with col2:
        s4a_ = 'Fiche Parent'
        s_s4a_ = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4a_}</p>"
        st.markdown(s_s4a_,unsafe_allow_html=True)
        st.markdown(FicheParent)

    s4b = 'Résumé'
    s_s4b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4b}</p>"
    st.markdown(s_s4b,unsafe_allow_html=True)
    st.markdown(Abstract)

    col1,col2,col3 = st.columns(3)
    with col1:
        s4d = 'Purpose'
        s_s4d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4d}</p>"
        st.markdown(s_s4d,unsafe_allow_html=True)
        st.markdown(Purpose)
    with col2:
        s4e = 'Status'
        s_s4e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4e}</p>"
        st.markdown(s_s4e,unsafe_allow_html=True)
        st.markdown(Status)
    with col3:
        s4f = 'Fréquence de maj'
        s_s4f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4f}</p>"
        st.markdown(s_s4f,unsafe_allow_html=True)
        st.markdown(Freq_maj)

    col1,col2,col3 =st.columns(3)
    with col1:
        s4c = 'Date (création)'
        s_s4c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4c}</p>"
        st.markdown(s_s4c,unsafe_allow_html=True)
        st.markdown(Date_creation)
    with col2:
        try:
            s4g = f'Date ({liste_dates[0][0]})'
            s_s4g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4g}</p>"
            st.markdown(s_s4g,unsafe_allow_html=True)
            st.markdown(liste_dates[0][1])
        except:
            pass
    with col3:
        try:
            s4h = f'Date ({liste_dates[1][0]})'
            s_s4h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4h}</p>"
            st.markdown(s_s4h,unsafe_allow_html=True)
            st.markdown(liste_dates[1][1])
        except:
            pass

with st.container(border=True):
    s5 = "MOTS CLES"
    s_s5 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s5}</p>"
    st.markdown(s_s5,unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)
    with col1:
        s5a = f'Thésaurus éventuel'
        s_s5a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5a}</p>"
        st.markdown(s_s5a,unsafe_allow_html=True)
    with col2:
        s5b = f'Type de mots clés'
        s_s5b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5b}</p>"
        st.markdown(s_s5b,unsafe_allow_html=True)
    with col3:
        s5c = f'Mots Clés'
        s_s5c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5c}</p>"
        st.markdown(s_s5c,unsafe_allow_html=True)

    for j in range(len(theme_thesaurus_motsCles)):
        col1,col2,col3 = st.columns(3)
        with col1:
            st.markdown(theme_thesaurus_motsCles[j][2])
        with col2:
            st.markdown(theme_thesaurus_motsCles[j][1])
        with col3:
            for i in range(len(theme_thesaurus_motsCles[j][0])):
                st.markdown(theme_thesaurus_motsCles[j][0][i])

with st.container(border=True):
    s6 = "CONTRAINTES"
    s_s6 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s6}</p>"
    st.markdown(s_s6,unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        s6a = "Limite d'Accès"
        s_s6a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6a}</p>"
        st.markdown(s_s6a,unsafe_allow_html=True)
        st.markdown(AccesContrainte)
    with col2:
        s6b = "Contrainte d'usage"
        s_s6b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6b}</p>"
        st.markdown(s_s6b,unsafe_allow_html=True)
        st.markdown(UseContrainte)
    with col3:
        s6c = "Limite d'Usage"
        s_s6c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6c}</p>"
        st.markdown(s_s6c,unsafe_allow_html=True)
        st.markdown(UseLimitation)
    with col4:
        s6d = "Limite d'Usage"
        s_s6d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6d}</p>"
        st.markdown(s_s6d,unsafe_allow_html=True)
        st.markdown(AutreContrainte)

with st.container(border=True):
    s7 = "DISTRIBUTION"
    s_s7 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s7}</p>"
    st.markdown(s_s7,unsafe_allow_html=True)

    col1,col2 = st.columns([0.7,0.3])
    with col1:
        s7b = "URL"
        s_s7b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7b}</p>"
        st.markdown(s_s7b,unsafe_allow_html=True)
        try:
            for x in range(len(Online_links)):
                    st.markdown(Online_links[x])
        except:
            pass
    with col2:
        s7c = "Protocole"
        s_s7c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7c}</p>"
        st.markdown(s_s7c,unsafe_allow_html=True)
        try:
            for x in range(len(Online_protocols)):
                    st.markdown(Online_protocols[x])
        except:
            pass
    
    col1,col2,col3 = st.columns([0.3,0.4,0.3])
    with col1:
        s7d = "Nom de la ressource"
        s_s7d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7d}</p>"
        st.markdown(s_s7d,unsafe_allow_html=True)
        try:
            for x in range(len(Online_nom)):
                    st.markdown(Online_nom[x])
        except:
            pass
    with col2:
        s7e = "Description de la ressource"
        s_s7e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7e}</p>"
        st.markdown(s_s7e,unsafe_allow_html=True)
        try:
            for x in range(len(Online_description)):
                    st.markdown(Online_description[x])
        except:
            pass
    with col3:
        s7a = "Format"
        s_s7a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7a}</p>"
        st.markdown(s_s7a,unsafe_allow_html=True)
        try:
            for x in range(len(Format)):
                    st.markdown(Format[x])
        except:
            pass

with st.container(border=True):
    s8 = "QUALITE"
    s_s8 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s8}</p>"
    st.markdown(s_s8,unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        s8a = "Niveau"
        s_s8a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8a}</p>"
        st.markdown(s_s8a,unsafe_allow_html=True)
        st.markdown(Niveau)

    with col2:
        s8b = "Conformité"
        s_s8b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8b}</p>"
        st.markdown(s_s8b,unsafe_allow_html=True)
        st.markdown(Conformite)

    s8c = "Généalogie"
    s_s8c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8c}</p>"
    st.markdown(s_s8c,unsafe_allow_html=True)
    st.markdown(Genealogie)