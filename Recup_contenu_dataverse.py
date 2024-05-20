import pandas as pd
import requests
import json

from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi

##########################  VARIABLES DE CONNEXION #######################
BASE_URL="https://data.indores.fr"
API_TOKEN="19f0769d-564f-44ac-809b-22853f186960"
##########################################################################

###################### CREATION CONNEXION ##############################
api = NativeApi(BASE_URL, API_TOKEN)
resp = api.get_info_version()
print(resp.json())

datarza = api.get_dataverse_contents("RZA")
liste_identifiers= []
data_rza = datarza.json()
print(data_rza)
"""for i in range(len(data_rza['data'])):
    try:
        t = "doi:" + data_rza['data'][i]["authority"] +'/'+ data_rza['data'][i]["identifier"]
        liste_identifiers.append(t)
    except:
        pass"""

#df = pd.DataFrame(liste_identifiers,columns=["Identifier"])
#df.to_csv("Enregistrements_dataverse_RZA")

