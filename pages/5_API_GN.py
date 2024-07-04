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
            st.button(':heavy_plus_sign:',on_click=increment_counter)
        with col03:
            st.markdown('')
            st.markdown('')
            st.button('R',on_click=reset_counter)
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
            xml_data = xmltodict.unparse(python_dict,pretty=True)

            with open(f"pages/data/{i}.xml","w") as xml_file:
                xml_file.write(xml_data)
                xml_file.close()

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
    sub_title8 = f"TITRE"
    s_sub_title8 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title8}</p>"
    st.markdown(s_sub_title8,unsafe_allow_html=True)

    ## TITRE ####################################################################################################################
    try:
        titre = str(df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:citation'][df['K4']=='gmd:title'][df['K6']=='#text:'].values[0])
        s_titre = f"<p style='font-size:20px;color:rgb(0,0,0)'>{titre}</p>"
        st.markdown(s_titre, unsafe_allow_html=True)
    except:
        titre = "Pas de titre"
        s_titre = f"<p style='font-size:20px;color:rgb(0,0,0)'>{titre}</p>"
        st.markdown(s_titre, unsafe_allow_html=True)

    sub_title9 = f"ABSTRACT"
    s_sub_title9 = f"<p style='font-size:25px;color:rgb{couleur_subtitles}'>{sub_title9}</p>"
    st.markdown(s_sub_title9,unsafe_allow_html=True)

    ## ABSTRACT #################################################################################################################
    try:
        abstract = str(df['Valeurs'][df['K0']=='gmd:identificationInfo'][df['K2']=='gmd:abstract'][df['K4']=='#text:'].values[0])
        s_abstract = f"<p style='font-size:20px;color:rgb(0,0,0)'>{abstract}</p>"
        st.markdown(s_abstract, unsafe_allow_html=True)
    except:
        abstract = "pas d'abstract"
        s_abstract = f"<p style='font-size:20px;color:rgb(0,0,0)'>{abstract}</p>"
        st.markdown(s_abstract, unsafe_allow_html=True)



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

df_ = df[['K0','K1','K2','K3','K4','K5','K6','K7','K8','Valeurs']]
st.dataframe(df_)

