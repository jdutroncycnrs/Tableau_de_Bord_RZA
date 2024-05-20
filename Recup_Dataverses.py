import pandas as pd
import requests
import json

from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi


#BASE_URL="https://dataverse-test.in2p3.fr"
#API_TOKEN= "77f73922-56ca-4889-8524-c623e65acaf4"

##########################  VARIABLES DE CONNEXION #######################
BASE_URL="https://data.indores.fr"
API_TOKEN="19f0769d-564f-44ac-809b-22853f186960"
##########################################################################

###################### CREATION CONNEXION ##############################
api = NativeApi(BASE_URL, API_TOKEN)
resp = api.get_info_version()
print(resp.json())

# Si le status indiqué est OK : c'est bon la connexion est établie

# On peut aller chercher le contenu du dataverse
# le status est rappelé puis on a une clé "data" dans laquelle on retrouve son contenu.
# Pour dataindores: d'autres sous-dataverses!


"""dataindores = api.get_dataverse_contents("dataindores")
print(json.dumps(dataindores.json(), indent=5))
data_indores = dataindores.json()
print(len(data_indores['data']))
print(data_indores['data'])"""

# Ici on récupère les noms de ces dataverses et les id 
# On crée un premier tableau avec ces élements
"""liste_dataverses_1= []
liste_ids = []
for d in range(len(data_indores['data'])):
    if data_indores['data'][d]['type']=="dataverse":
        liste_dataverses_1.append(data_indores['data'][d]['title'])
        liste_ids.append(data_indores['data'][d]['id'])
df_liste_dataverses_1=pd.DataFrame(data=[liste_dataverses_1,liste_ids], index=['Dataverses_niv1','Ids'])
df_liste_dataverses_1=df_liste_dataverses_1.T"""

# A partir de ce tableau, pour chacun des dataverses répertoriés (niv1), on récupère les noms des sous-dataverses (niv2) 
# On enregistre ces infos dans un csv
"""liste = []
for i in range(len(df_liste_dataverses_1)):
    datav = api.get_dataverse_contents(df_liste_dataverses_1.loc[i,'Ids'])
    datav_dv = datav.json()
    liste_dataverses_2 = []
    for d in range(len(datav_dv['data'])):
        try:
            if datav_dv['data'][d]['type']=="dataverse":
                liste_dataverses_2.append(datav_dv['data'][d]['title'])
        except:
                liste_dataverses_2.append()
    liste.append(liste_dataverses_2)
print(liste)

df_liste_dataverses_1['Dataverses_niv2']=liste
df_liste_dataverses_1.to_csv("liste_dataverses")"""

