import pandas as pd
import streamlit as st
import ast


Selection_ZA = " Zone atelier Alpes"
liste_col_to_keep = ['Store','Entrepot','Titre et auteurs','Uri']
liste_col_to_keep2 = ['Store','Entrepot','Titre']

data_hal = pd.read_csv("pages/data/Hal/Contenu_HAL_complet.csv", index_col=[0])
data_hal_ = data_hal[data_hal['Entrepot']==Selection_ZA]
data_hal__ = data_hal_[data_hal_['Type de document']=='ART']
data_hal_k = data_hal__[liste_col_to_keep]
data_hal_k.reset_index(inplace=True)
data_hal_k.drop(columns='index', inplace=True)
data_hal_k.to_csv("pages/data/temp/HAL_ZAA.csv")
st.dataframe(data_hal_k)


data_Indores = pd.read_csv("pages/data/Contenu_DataInDoRES2.csv",index_col=[0])
data_Indores['Store']='Data.InDoRES'
data_Indores_ = data_Indores[data_Indores['Entrepot']==Selection_ZA]
data_Indores_k =data_Indores_[liste_col_to_keep2]

data_RDG = pd.read_csv("pages/data/rechercheDataGouv/Contenu_RDG_complet.csv", index_col=[0])
data_RDG_ = data_RDG[data_RDG['Entrepot']==Selection_ZA]
data_RDG_k = data_RDG_[liste_col_to_keep2]

data_dryad = pd.read_csv("pages/data/Dryad/Contenu_DRYAD_complet.csv", index_col=[0])
data_dryad['Source'] = "DRYAD"
data_dryad_ = data_dryad[data_dryad['Entrepot']==Selection_ZA]
data_dryad_k = data_dryad_[liste_col_to_keep2]

data_zenodo = pd.read_csv("pages/data/Zenodo/Contenu_ZENODO_complet.csv", index_col=[0])
data_zenodo['Source'] = 'ZENODO'
data_zenodo_ = data_zenodo[data_zenodo['Entrepot']==Selection_ZA]
data_zenodo_k = data_zenodo_[liste_col_to_keep2]

# le filtre zenodo est à améliorer

data_ZAA = pd.concat([data_Indores_k,data_RDG_k,data_dryad_k,data_zenodo_k], axis=0)
data_ZAA.reset_index(inplace=True)
data_ZAA.drop(columns='index', inplace=True)
data_ZAA.to_csv("pages/data/temp/ENTREPOTS_ZAA.csv")
st.dataframe(data_ZAA)

def transfo(input_string):
    # Use ast.literal_eval to safely evaluate the string as a Python expression
    return ast.literal_eval(input_string)
def transfo0(input_string):
    # Use ast.literal_eval to safely evaluate the string as a Python expression
    return input_string.replace("' '","','")


liste_col_to_keep3 = ['Store','Entrepot','Titre', 'Url', 'Noms des fichiers','Titre parents','Titre children','Titre brothersAndSisters', 'Titre facts']
data_catInDoRES = pd.read_csv("pages/data/infos_MD2/tableau_complet.csv", index_col=[0])
for i in range(len(data_catInDoRES)):
    if data_catInDoRES.loc[i,'Url']=="":
        data_catInDoRES.loc[i,'Url']="[]"
data_catInDoRES['Url'] = data_catInDoRES['Url'].apply(transfo0)
data_catInDoRES['Url'] = data_catInDoRES['Url'].apply(transfo)
data_catInDoRES_ = data_catInDoRES[data_catInDoRES['GroupeEtMention']=='zaa']
data_catInDoRES_.reset_index(inplace=True)
data_catInDoRES_.drop(columns='index', inplace=True)

data_catInDoRES_R = pd.read_csv("pages/data/infos_MD2/tableau_fichiers_ressources.csv", index_col=[0])

data_catInDoRES_A = pd.read_csv("pages/data/infos_MD2/tableau_fichiers_attachements.csv", index_col=[0])

df_catInDoRES = pd.merge(data_catInDoRES_R,data_catInDoRES_A, on='Identifiant', how='inner')
df_catInDoRES_zaa = pd.merge(df_catInDoRES,data_catInDoRES_, on='Identifiant', how='inner')

liste_Identifiants = df_catInDoRES_zaa['Identifiant'].values
data_catInDoRES_filtered = data_catInDoRES_[~data_catInDoRES_['Identifiant'].isin(liste_Identifiants)]

df_catInDoRES_zaa_ = pd.concat([df_catInDoRES_zaa,data_catInDoRES_filtered], axis=0)
df_catInDoRES_zaa_.reset_index(inplace=True)
df_catInDoRES_zaa_.drop(columns='index', inplace=True)
df_catInDoRES_zaa_['Store']="Cat.InDoRES"
df_catInDoRES_zaa_['Entrepot']=Selection_ZA
df_catInDoRES_zaa__ = df_catInDoRES_zaa_[liste_col_to_keep3]
df_catInDoRES_zaa__.to_csv("pages/data/temp/CATALOGUE_ZAA.csv")
st.dataframe(df_catInDoRES_zaa__)