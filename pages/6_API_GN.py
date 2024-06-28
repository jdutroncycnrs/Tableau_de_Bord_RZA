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

######################## URL de l'API ##############################

url = "https://cat.indores.fr/geonetwork/srv/api/records/"

####################################################################

headers = {"accept":"application/json",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}

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

data = pd.read_csv(fichier,index_col=[0])

if 'count' not in st.session_state:
    st.session_state.count = 0
def increment_counter():
    st.session_state.count += 1
def reset_counter():
    st.session_state.count = 0

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
    st.button('reset',on_click=reset_counter)


i= piq_one
st.write(piq_one)
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

df_ = df[['K0','K1','Valeurs']]

st.dataframe(df_)