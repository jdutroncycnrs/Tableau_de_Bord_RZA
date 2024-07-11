import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import xmltodict
import dicttoxml
import sys
import re
pd.options.mode.chained_assignment = None

########### TITRE DE L'ONGLET ######################################
st.set_page_config(
    page_title="GeoNetwork",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)
####################################################################

fichier= "pages/data/uuid_cat_InDoRes_clean_compared.csv"

####################################################################

data = pd.read_csv(fichier,index_col=[0])

######################## URL de l'API ##############################

url = "https://cat.indores.fr/geonetwork/srv/api/records/"

####################################################################

headers = {"accept":"application/json",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}

couleur_subtitles = (250,100,0)

try:
    df_fair = pd.read_csv('test_fair.csv', index_col=[0])
except:
    df_fair = pd.DataFrame(columns=['identifieur','F1','F2','F3','F4','A1_1','A1_2','A2','I1','I2','I3','R1_1','R1_2','R1_3','Validation'])

####################################################################

def transcript_json(json_data, file, prefix=""):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, dict) or isinstance(value, list):
                transcript_json(value,file, f"{prefix}.{key}" if prefix else key)
            else:
                #print(f"{prefix}.{key}: {value}" if prefix else f"{key}: {value}")
                file.write(f"{prefix}.{key}:!{value}," if prefix else f"{key}:!{value},")
    elif isinstance(json_data, list):
        for item in json_data:
            transcript_json(item,file, prefix)
    else:
        #print(f"{prefix}: {json_data}" if prefix else f"{json_data}")
        file.write(f"{prefix}:!{json_data}," if prefix else f"{json_data},")


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


#################################################################################################################################
#################################################################################################################################
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        sub_title1 = "IDENTIFIEUR"
        s_sub_title1 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title1}</p>"
        st.markdown(s_sub_title1,unsafe_allow_html=True)

        col01,col02,col03 = st.columns([0.8,0.1,0.1])
        with col01:
            piq_one = st.selectbox(label='',options=data['uuid_cat_InDoRes'], index=st.session_state.count)
        with col02:
            st.markdown('')
            st.markdown('')
            button1 = st.button(':heavy_plus_sign:',on_click=increment_counter)
        with col03:
            st.markdown('')
            st.markdown('')
            button2 =st.button('R',on_click=reset_counter)
        ####################################################################################################
        ## RECUPERATION DONNEES
        ####################################################################################################
        # IDENTIFIEUR
        i= piq_one
        ###################################################################################################
        try:
            df = pd.read_csv(f'pages/data/{i}.csv',index_col=[0])
        except:
            url_ = url + i
            resp = requests.get(url_,headers=headers)
            rr=resp.json()
            test = {}
            test["gmd:MD_Metadata"]=rr

            with open(f"pages/data/{i}.json", "w") as f:
                json.dump(test, f, indent=4)

            ############# VERS XML
            with open(f"pages/data/{i}.json","r") as file:
                python_dict=json.load(file)
                
            # Convert the JSON data to XML 
            try:
                xml_data = xmltodict.unparse(python_dict,pretty=True)

                with open(f"pages/data/{i}.xml","w") as xml_file:
                    xml_file.write(xml_data)
                    xml_file.close()
            except:
                pass

            with open(f'pages/data/{i}.json', 'r') as f:
                data = json.load(f)

            # Call the function to print concatenated keys and values
            with open(f'pages/data/{i}.txt', 'w') as file:
                transcript_json(data, file)

            with open(f'pages/data/{i}.txt', 'r') as f:
                d = f.read()

            listi = re.split(',',d)
            df = pd.DataFrame(listi[0:-1], columns=['Results'])
            for u in range(len(df)):
                p = re.split('!',df.loc[u,'Results'])
                try:
                    df.loc[u,'Valeurs']=p[1]
                except:
                    pass
                try:
                    df.loc[u,'Clés']=p[0].replace('.','/')
                except:
                    pass
            for j in range(len(df)):
                pp = re.split('/',df.loc[j,'Clés'])
                for k in range(15):
                    try:
                        df.loc[j,f'K{k}']=pp[k+1]
                    except:
                        pass
            df.to_csv(f'pages/data/{i}.csv')
    with col2:
        ## DATESTAMP ##############################################################################
        try:
            datestamp = str(df['Valeurs'][df['K0']=='gmd:dateStamp'][df['K2']=='#text:'].values[0])
            sub_title2 = "DATESTAMP"
            s_sub_title2 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title2}</p>"
            st.markdown(s_sub_title2,unsafe_allow_html=True)
            st.metric(label='', value=datestamp)
        except:
            sub_title2 = "DATESTAMP"
            s_sub_title2 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title2}</p>"
            st.markdown(s_sub_title2,unsafe_allow_html=True)
            st.metric(label='', value="pas de datestamp")
        
    
    ########################################################################################################
    col1,col2 = st.columns(2)
    with col1:
        ## STANDARD LANGUE ##############################################################################
        try:
            Standard_langue = str(df['Valeurs'][df['K0']=='gmd:language'][df['K2']=='@xmlns:gco:'].values[0])
            try:
            ## LANGUE #######################################################################################
                langue = str(df['Valeurs'][df['K0']=='gmd:language'][df['K2']=='#text:'].values[0])
                sub_title3 = f"LANGUE ({Standard_langue})"
                s_sub_title3 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title3}</p>"
                st.markdown(s_sub_title3,unsafe_allow_html=True)
                st.metric(label='', value= langue)
            #################################################################################################
            except:
                sub_title3 = f"LANGUE ({Standard_langue})"
                s_sub_title3 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title3}</p>"
                st.markdown(s_sub_title3,unsafe_allow_html=True)
                st.metric(label='', value= "pas de langue")
        except:
            try:
            ## LANGUE #######################################################################################
                langue = str(df['Valeurs'][df['K0']=='gmd:language'][df['K2']=='#text:'].values[0])
                sub_title3 = f"LANGUE (pas de standard)"
                s_sub_title3 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title3}</p>"
                st.markdown(s_sub_title3,unsafe_allow_html=True)
                st.metric(label='', value= langue)
            #################################################################################################
            except:
                sub_title3 = f"LANGUE (pas de standard)"
                s_sub_title3 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title3}</p>"
                st.markdown(s_sub_title3,unsafe_allow_html=True)
                st.metric(label='', value= "pas de langue")

    with col2:
        ## ENCODAGE #####################################################################################
        try:
            encodage = str(df['Valeurs'][df['K0']=='gmd:characterSet'][df['K2']=='@codeListValue:'].values[0])
            sub_title4 = "ENCODAGE"
            s_sub_title4 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title4}</p>"
            st.markdown(s_sub_title4,unsafe_allow_html=True)
            st.metric(label='', value=encodage)
        except:
            sub_title4 = "ENCODAGE"
            s_sub_title4 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title4}</p>"
            st.markdown(s_sub_title4,unsafe_allow_html=True)
            st.metric(label='', value="pas d'encodage")

    ########################################################################################################
    col1,col2 = st.columns(2)
    with col1:
        ## VERSION STANDARD ################################################################################
        try:
            version_standard = str(df['Valeurs'][df['K0']=='gmd:metadataStandardVersion'][df['K2']=='#text:'].values[0])
            ## STANDARD MD #####################################################################################
            try:
                standard_MD = str(df['Valeurs'][df['K0']=='gmd:metadataStandardName'][df['K2']=='#text:'].values[0])
                sub_title5 = f"STANDARD MD / VERSION {version_standard}"
                s_sub_title5 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title5}</p>"
                st.markdown(s_sub_title5,unsafe_allow_html=True)
                st.metric(label='', value=standard_MD)
            except:
                sub_title5 = f"STANDARD MD / VERSION {version_standard}"
                s_sub_title5 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title5}</p>"
                st.markdown(s_sub_title5,unsafe_allow_html=True)
                st.metric(label='', value="pas de standard")

        except:
            version_standard = 'inconnue'
            try:
                standard_MD = str(df['Valeurs'][df['K0']=='gmd:metadataStandardName'][df['K2']=='#text:'].values[0])
                sub_title5 = f"STANDARD MD / VERSION {version_standard}"
                s_sub_title5 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title5}</p>"
                st.markdown(s_sub_title5,unsafe_allow_html=True)
                st.metric(label='', value=standard_MD)
            except:
                sub_title5 = f"STANDARD MD / VERSION {version_standard}"
                s_sub_title5 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title5}</p>"
                st.markdown(s_sub_title5,unsafe_allow_html=True)
                st.metric(label='', value="pas de standard")

    with col2:
        ## REF STANDARD ####################################################################################
        try:
            standard_ref = str(df['Valeurs'][df['K0']=='gmd:referenceSystemInfo'][df['K2']=='gmd:referenceSystemIdentifier'][df['K4']=='gmd:code'][df['K6']=='@xmlns:gco:'].values[0])
            try:
                ## REF #############################################################################################
                ref = str(df['Valeurs'][df['K0']=='gmd:referenceSystemInfo'][df['K2']=='gmd:referenceSystemIdentifier'][df['K4']=='gmd:code'][df['K6']=='#text:'].values[0])
                sub_title7 = "REF"+f"({standard_ref})"
                s_sub_title7 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title7}</p>"
                st.markdown(s_sub_title7,unsafe_allow_html=True)
                st.metric(label='', value=ref)
            except:
                sub_title7 = "REF"+f"({standard_ref})"
                s_sub_title7 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title7}</p>"
                st.markdown(s_sub_title7,unsafe_allow_html=True)
                st.metric(label='', value="pas de ref")
        except:
            standard_ref = "standard inconnu"
            try:
                ## REF #############################################################################################
                ref = str(df['Valeurs'][df['K0']=='gmd:referenceSystemInfo'][df['K2']=='gmd:referenceSystemIdentifier'][df['K4']=='gmd:code'][df['K6']=='#text:'].values[0])
                sub_title7 = "REF"+f"({standard_ref})"
                s_sub_title7 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title7}</p>"
                st.markdown(s_sub_title7,unsafe_allow_html=True)
                st.metric(label='', value=ref)
            except:
                sub_title7 = "REF"+f"({standard_ref})"
                s_sub_title7 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title7}</p>"
                st.markdown(s_sub_title7,unsafe_allow_html=True)
                st.metric(label='', value="pas de ref")



#################################################################################################################################
#################################################################################################################################
with st.container(border=True):
    id = i
    sub_title8 = f"TITRE / ID: {i}"
    s_sub_title8 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title8}</p>"
    st.markdown(s_sub_title8,unsafe_allow_html=True)

    ## TITRE ####################################################################################################################
    try:
        titre = str(df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:citation'][df['K4']=='gmd:title'][df['K6']=='#text:'].values[0])
        s_titre = f"<p style='font-size:25px;color:rgb(0,0,0)'>{titre}</p>"
        st.markdown(s_titre, unsafe_allow_html=True)
    except:
        titre = "Pas de titre"
        s_titre = f"<p style='font-size:25px;color:rgb(0,0,0)'>{titre}</p>"
        st.markdown(s_titre, unsafe_allow_html=True)

    sub_title9 = f"ABSTRACT"
    s_sub_title9 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title9}</p>"
    st.markdown(s_sub_title9,unsafe_allow_html=True)

    ## ABSTRACT #################################################################################################################
    try:
        abstract = str(df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:abstract'][df['K4']=='#text:'].values[0])
        s_abstract = f"<p style='font-size:25px;color:rgb(0,0,0)'>{abstract}</p>"
        st.markdown(s_abstract, unsafe_allow_html=True)
    except:
        abstract = "pas d'abstract"
        s_abstract = f"<p style='font-size:25px;color:rgb(0,0,0)'>{abstract}</p>"
        st.markdown(s_abstract, unsafe_allow_html=True)


    sub_title9 = f"DATES RESSOURCES"
    s_sub_title9 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title9}</p>"
    st.markdown(s_sub_title9,unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    try:
        status_date = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:citation'][df['K4']=='gmd:date'][df['K6']=='gmd:dateType'][df['K7']=='gmd:CI_DateTypeCode'][df['K8']=='@codeListValue:'].values
    except:
        pass
    try:
        dates = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:citation'][df['K4']=='gmd:date'][df['K6']=='gmd:date'][df['K8']=='#text:'].values
    except:
        pass
    with col1:
        try:
            date0 = dates[0]
            st.metric(label=status_date[0], value=date0)
        except:
            try:
                date0 = "Non renseignée"
                st.metric(label=status_date[0], value=date0)
            except:
                pass
    with col2:
        try:
            date1 = dates[1]
            st.metric(label=status_date[1], value=date1)
        except:
            try:
                date1 = "Non renseignée"
                st.metric(label=status_date[1], value=date1)
            except:
                pass
    with col3:
        try:
            date2= dates[2]
            st.metric(label=status_date[2], value=date2)
        except:
            try:
                date2 = "Non renseignée"
                st.metric(label=status_date[2], value=date2)
            except:
                pass

    col1,col2 = st.columns(2)
    with col1:
        try:
            edition = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:citation'][df['K4']=='gmd:edition'][df['K6']=='#text:'].values[0]
            sub_title10 = f"EDITION"
            s_sub_title10 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title10}</p>"
            st.markdown(s_sub_title10,unsafe_allow_html=True)
            st.metric(label="", value=edition)
        except:
            edition = "non renseignée"
            sub_title10 = f"EDITION"
            s_sub_title10 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title10}</p>"
            st.markdown(s_sub_title10,unsafe_allow_html=True)
            st.metric(label="", value=edition)
    with col2:
        try:
            presentation_form = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:citation'][df['K4']=='gmd:presentationForm'][df['K6']=='@codeListValue:'].values[0]
            sub_title11 = f"FORME DE PRESENTATION"
            s_sub_title11 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title11}</p>"
            st.markdown(s_sub_title11,unsafe_allow_html=True)
            st.metric(label="", value=presentation_form)
        except:
            presentation_form = "non renseignée"
            sub_title11 = f"FORME DE PRESENTATION"
            s_sub_title11 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title11}</p>"
            st.markdown(s_sub_title11,unsafe_allow_html=True)
            st.metric(label="", value=presentation_form)

    sub_title12 = f"POINTS DE CONTACT"
    s_sub_title12 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title12}</p>"
    st.markdown(s_sub_title12,unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        try:
            individual_name = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:individualName'][df['K6']=='#text:'].values[0]
            st.metric(label="Nom du contact", value=individual_name)
        except:
            individual_name = "Non renseigné"
            st.metric(label="Nom du contact", value=individual_name)
    with col2:
        try:
            orga_name = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:organisationName'][df['K6']=='#text:'].values[0]
            st.metric(label="Orga du contact", value=orga_name)
        except:
            orga_name = "Non renseignée"
            st.metric(label="Orga du contact", value=orga_name)
    with col3:
        try:
            position = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:positionName'][df['K6']=='#text:'].values[0]
            st.metric(label="Position du contact", value=position)
        except:
            position = "Non renseignée"
            st.metric(label="Position du contact", value=position)
    with col4:
        try:
            role = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:role'][df['K6']=='@codeListValue:'].values[0]
            st.metric(label="Rôle du contact", value=role)
        except:
            role = "Non renseigné"
            st.metric(label="Rôle du contact", value=role)

    sub_title13 = f"INFOS CONTACT"
    s_sub_title13 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title13}</p>"
    st.markdown(s_sub_title13,unsafe_allow_html=True)

    col1,col2= st.columns([0.2,0.8])
    with col1:
        try:
            telephone = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:phone'][df['K8']=='gmd:voice'][df['K10']=='#text:'].values[0]
            st.metric(label="Téléphone du contact", value=telephone)
        except:
            telephone = "Non renseigné"
            st.metric(label="Téléphonedu contact", value=telephone)
    with col2:
        try:
            adresse = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:address'][df['K8']=='gmd:deliveryPoint'][df['K10']=='#text:'].values[0]
        except:
            adresse = "____"
        try:    
            code_postal = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:address'][df['K8']=='gmd:postalCode'][df['K10']=='#text:'].values[0]
        except:
            code_postal = "#####" 
        try:   
            city = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:address'][df['K8']=='gmd:city'][df['K10']=='#text:'].values[0]
        except:
            city = "XXXX"
        try:    
            area = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:address'][df['K8']=='gmd:administrativeArea'][df['K10']=='#text:'].values[0]
        except:
            area = "/..../"
        try:
            country = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:address'][df['K8']=='gmd:country'][df['K10']=='#text:'].values[0]
        except:
            country = "No country"
        adresse_complete = str(adresse) +' '+ str(code_postal) +' '+ str(city) +' '+ str(area) +' '+ str(country)
        st.metric(label="Adresse du contact", value=adresse_complete)

    try:
        email = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:address'][df['K8']=='gmd:electronicMailAddress'][df['K10']=='#text:'].values[0]
        st.metric(label="Email du contact", value=email)
    except:
        pass

#################################################################################################################################
#################################################################################################################################
with st.container(border=True):
    sub_title14 = f"ONLINE RESSOURCE"
    s_sub_title14 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title14}</p>"
    st.markdown(s_sub_title14,unsafe_allow_html=True)

    col1,col2 = st.columns([0.6,0.4])
    with col1:
        try:
            url = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:onlineResource'][df['K8']=='gmd:linkage'][df['K9']=='gmd:URL:'].values[0]
            s_url = f"<p style='font-size:25px;color:rgb(0,0,200)'>{url}</p>"
            st.markdown(s_url, unsafe_allow_html=True)
        except:
            url = 'Pas de lien'
            st.metric(label="URL", value=url)
    with col2:
        try:
            protocol = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:onlineResource'][df['K8']=='gmd:protocol'][df['K10']=='#text:'].values[0]
            st.metric(label="Protocole", value=protocol)
        except:
            protocol = 'Pas de protocole renseigné'
            st.metric(label="Protocole", value=protocol)

    col1,col2,col3 = st.columns([0.4,0.4,0.2])
    with col1:
        try:
            nom_url = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:onlineResource'][df['K8']=='gmd:name'][df['K10']=='#text:'].values[0]
            st.metric(label="Attachement", value=nom_url)
        except:
            nom_url = 'Non renseigné'
            st.metric(label="Attachement", value=nom_url)
    with col2:
        try:
            description_url = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:onlineResource'][df['K8']=='gmd:description'][df['K10']=='#text:'].values[0]
            st.metric(label="Description", value=description_url)
        except:
            description_url = 'Pas de description'
            st.metric(label="Description", value=description_url)
    with col3:
        try:
            fonction_url = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:pointOfContact'][df['K4']=='gmd:contactInfo'][df['K6']=='gmd:onlineResource'][df['K8']=='gmd:function'][df['K10']=='@codeListValue:'].values[0]
            st.metric(label="Fonction", value=fonction_url)
        except:
            fonction_url = 'Non renseigné'
            st.metric(label="Fonction", value=fonction_url)

    col1,col2 = st.columns([0.4,0.6])
    with col1:
        try:
            maintenance_freq = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:resourceMaintenance'][df['K4']=='gmd:maintenanceAndUpdateFrequency'][df['K6']=='@codeListValue:'].values[0]
            st.metric(label="Fréquence de la maintenance", value=maintenance_freq)
        except:
            maintenance_freq = 'Non renseignée'
            st.metric(label="Fréquence de la maintenance", value=maintenance_freq)
    with col2:
        try:
            period_maintenance = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:resourceMaintenance'][df['K4']=='gmd:userDefinedMaintenanceFrequency'][df['K6']=='#text:'].values[0]
            st.metric(label="Période définie par l'utilisateur", value=period_maintenance)
        except:
            period_maintenance = 'Non renseignée'
            st.metric(label="Période définie par l'utilisateur", value=period_maintenance)

    col1,col2,col3,col4 = st.columns([0.25,0.25,0.25,0.25])
    with col1:
        try:
            use_limitation = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:resourceConstraints'][df['K4']=='gmd:useLimitation'][df['K6']=='#text:'].values[0]
            s_useLimitation = f"<p style='font-size:25px;color:rgb(0,0,200)'>{use_limitation}</p>"
            st.markdown(s_useLimitation, unsafe_allow_html=True)
        except:
            use_limitation = 'Non renseignée'
            st.metric(label="Limite d'usage", value=use_limitation)
    with col2:
        try:
            contrainte_access = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:resourceConstraints'][df['K4']=='gmd:accessConstraints'][df['K6']=='@codeListValue:'].values[0]
            st.metric(label="Contrainte d'accès", value=contrainte_access)
        except:
            contrainte_access = 'Non renseignée'
            st.metric(label="Contrainte d'accès", value=contrainte_access)
    with col3:
        try:
            contrainte_usage = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:resourceConstraints'][df['K4']=='gmd:useConstraints'][df['K6']=='@codeListValue:'].values[0]
            st.metric(label="Contrainte d'usage", value=contrainte_usage)
        except:
            contrainte_usage = 'Non renseignée'
            st.metric(label="Contrainte d'usage", value=contrainte_usage)
    with col4:
        try:
            autres_contraintes = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:resourceConstraints'][df['K4']=='gmd:otherConstraints'][df['K6']=='#text:'].values
            if len(autres_contraintes)>1:
                contraintes = autres_contraintes[0]
                for x in range(1,len(autres_contraintes)):
                    contraintes += '/ ' + autres_contraintes[x]
                s_autres_contraintes = f"<p style='font-size:25px;color:rgb(0,0,200)'>{contraintes}</p>"
                st.markdown(s_autres_contraintes, unsafe_allow_html=True)
            else:
                s_autres_contraintes = f"<p style='font-size:25px;color:rgb(0,0,200)'>{autres_contraintes[0]}</p>"
                st.markdown(s_autres_contraintes, unsafe_allow_html=True)

        except:
            contraintes = 'Non renseigné'
            s_autres_contraintes = f"<p style='font-size:25px;color:rgb(0,0,200)'>{contraintes}</p>"
            st.markdown(s_autres_contraintes, unsafe_allow_html=True)


#################################################################################################################################
#################################################################################################################################
with st.container(border=True):
    sub_title = f"THEMATIQUE"
    s_sub_title = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title}</p>"
    st.markdown(s_sub_title,unsafe_allow_html=True)

    try:
        topic_category = df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:topicCategory'].values[0]
        st.metric(label="", value=topic_category)
    except:
        topic_category = "Pas de thématique renseignée!"
        st.metric(label="", value=topic_category)

#################################################################################################################################
#################################################################################################################################
with st.container(border=True):
    sub_title = f"FORMAT"
    s_sub_title = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title}</p>"
    st.markdown(s_sub_title,unsafe_allow_html=True)


#################################################################################################################################
#################################################################################################################################
with st.container(border=True):
    sub_title = f"SCOPE"
    s_sub_title = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title}</p>"
    st.markdown(s_sub_title,unsafe_allow_html=True)


#################################################################################################################################
#################################################################################################################################
with st.container(border=True):

    sub_title = f"EVALUATION FAIR"
    s_sub_title = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title}</p>"
    st.markdown(s_sub_title,unsafe_allow_html=True)

    
    def reset_checkboxes():
        st.session_state.F1 = False
        st.session_state.F2 = False
        st.session_state.F3 = False
        st.session_state.F4 = False
        st.session_state.A1_1 = False
        st.session_state.A1_2 = False
        st.session_state.A2 = False
        st.session_state.I1 = False
        st.session_state.I2 = False
        st.session_state.I3 = False
        st.session_state.R1_1 = False
        st.session_state.R1_2 = False
        st.session_state.R1_3 = False
        st.session_state.Validation = False

    if button1 or button2:
        reset_checkboxes()

    if 'F1' not in st.session_state:
        st.session_state.F1 = False
    if 'F2' not in st.session_state:
        st.session_state.F2 = False
    if 'F3' not in st.session_state:
        st.session_state.F3 = False
    if 'F4' not in st.session_state:
        st.session_state.F4 = False
    if 'A1_1' not in st.session_state:
        st.session_state.A1_1 = False
    if 'A1_2' not in st.session_state:
        st.session_state.A1_2 = False
    if 'A2' not in st.session_state:
        st.session_state.A2 = False
    if 'I1' not in st.session_state:
        st.session_state.I1 = False
    if 'I2' not in st.session_state:
        st.session_state.I2 = False      
    if 'I3' not in st.session_state:
        st.session_state.I3 = False
    if 'R1_1' not in st.session_state:
        st.session_state.R1_1 = False
    if 'R1_2' not in st.session_state:
        st.session_state.R1_2 = False
    if 'R1_3' not in st.session_state:
        st.session_state.R1_3 = False
    if 'V' not in st.session_state:
        st.session_state.Validation = False

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        F1 = st.checkbox("F1 Unique_ID",value=st.session_state.F1,key='F1')
        F2 = st.checkbox("F2 Riche_MD",value=st.session_state.F2,key='F2')
        F3 = st.checkbox("F3 ID_des_Datas",value=st.session_state.F3,key='F3')
        F4 = st.checkbox("F4 Indexing",value=st.session_state.F4,key='F4')
    with col2:
        A1_1 = st.checkbox("A1.1 URL_data/gratuit",value=st.session_state.A1_1,key='A1_1')
        A1_2 = st.checkbox("A1.2 URL_data/auth",value=st.session_state.A1_2,key='A1_2')
        A2 = st.checkbox("A2 MD_access_without_data",value=st.session_state.A2,key='A2')
    with col3:
        I1 = st.checkbox("I1 FAIR_Format",value=st.session_state.I1,key='I1')
        I2 = st.checkbox("I2 Vocabularies",value=st.session_state.I2,key='I2')
        I3 = st.checkbox("I3 Autres_refs",value=st.session_state.I3,key='I3')
    with col4:
        R1_1 = st.checkbox("R1.1 Droits",value=st.session_state.R1_1,key='R1_1')
        R1_2 = st.checkbox("R1.2 Genealogie",value=st.session_state.R1_2,key='R1_2')
        R1_3 = st.checkbox("R1.3 Structuration",value=st.session_state.R1_3,key='R1_3')

    Validation = st.checkbox("Validation",value=st.session_state.Validation,key='V')

    dfi = pd.DataFrame(data=[[i, F1,F2,F3,F4,A1_1,A1_2,A2,I1,I2,I3,R1_1,R1_2,R1_3,Validation]],columns=['identifieur','F1','F2','F3','F4','A1_1','A1_2','A2','I1','I2','I3','R1_1','R1_2','R1_3','Validation'])

    df_fair_i = pd.concat([dfi, df_fair], axis=0)
    df_fair = df_fair_i
    df_fair.drop_duplicates(subset='identifieur', inplace=True)
    df_fair.to_csv('test_fair.csv')

st.sidebar.markdown(f'FAIR')
st.sidebar.table(df_fair[df_fair['identifieur']==i].T)

st.dataframe(df_fair)
try:
    df_ = df[['K0','K1','K2','K3','K4','K5','K6','K7','K8','K9','K10','Valeurs']]
    #st.dataframe(df_)
except:
    pass