#authority = "10.48579"
#st.write(liste_identifiers_dataset)
        
#for identifier in liste_identifiers_dataset:
#    dataset = api.get_dataset(identifier=f"doi:{authority}/{identifier}")
#    dataset_ = dataset.json()
#    st.write(dataset_["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"][0]["value"])     

import pandas as pd

data = pd.read_csv('pages/data/infos_MD/infos_groupes.csv', index_col=[0])
data_sorted = data.sort_values(by='Identifiant').reset_index(drop=True)

uuids = pd.read_csv('pages/data/uuids/uuid_cat_InDoRes_clean_2024-08-01.csv', index_col=[0])
uuids.drop_duplicates(keep='first', inplace=True)
uuids_sorted = uuids.sort_values(by='uuid_cat_InDoRes').reset_index(drop=True)

liste_uuids = uuids_sorted['uuid_cat_InDoRes'].values
print(len(liste_uuids))

for i in range(len(data_sorted)):
    if data_sorted.loc[i, 'Identifiant'] in liste_uuids:
        data_sorted.loc[i, 'IN']=True
    else:
        data_sorted.loc[i, 'IN']=False

data_bis = data_sorted[data_sorted['IN']==True]


data_bis.drop_duplicates(keep='first', inplace=True)
data_bis.reset_index(inplace=True, drop=True)

data_bis.to_csv('pages/data/infos_MD/infos_groupes2.csv')