import pandas as pd
import streamlit as st


Selection_ZA = " Zone atelier Alpes"

data_hal = pd.read_csv("pages/data/Hal/Contenu_HAL_complet.csv", index_col=[0])
data_hal_ = data_hal[data_hal['Entrepot']==Selection_ZA]
st.dataframe(data_hal_)

liste_col_to_keep = ['Entrepot','Source','Titre']

data_Indores = pd.read_csv("pages/data/Contenu_DataInDoRES2.csv",index_col=[0])
data_Indores['Source']='Data.InDoRES'
data_Indores_ = data_Indores[data_Indores['Entrepot']==Selection_ZA]
data_Indores_k =data_Indores_[liste_col_to_keep]

data_osug = pd.read_csv("pages/data/rechercheDataGouv/Contenu_RDG__Data_Repository_Grenoble_Alpes___OSUG.csv", index_col=[0])
data_osug['Source'] = data_osug['Entrepot']
data_osug['Entrepot'] = " Zone atelier Alpes"
data_osug_k = data_osug[liste_col_to_keep]

# il manque le nom de l'entrepôt de filtre
# car il manque le filtre...

# + à venir un contenu_complet?


data_dryad = pd.read_csv("pages/data/Dryad/Contenu_DRYAD_complet.csv", index_col=[0])
data_dryad['Source'] = "DRYAD"
data_dryad_ = data_dryad[data_dryad['Entrepot']==Selection_ZA]
data_dryad_k = data_dryad_[liste_col_to_keep]

data_zenodo = pd.read_csv("pages/data/Zenodo/Contenu_ZENODO_complet.csv", index_col=[0])
data_zenodo['Source'] = 'ZENODO'
data_zenodo_ = data_zenodo[data_zenodo['Entrepot']==Selection_ZA]
data_zenodo_k = data_zenodo_[liste_col_to_keep]

# le filtre zenodo est à améliorer

data_ZAA = pd.concat([data_Indores_k,data_osug_k,data_dryad_k,data_zenodo_k], axis=0)
data_ZAA.reset_index(inplace=True)
data_ZAA.drop(columns='index', inplace=True)
st.table(data_ZAA)