import pandas as pd
import requests
import json

from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi

import datetime
import numpy as np


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






d = datetime.date.today()
fichier = f'tableau_dataverses-{d}.csv'
dat = pd.read_csv(f"pages/data/{fichier}")
dat.drop(columns=['Unnamed: 0'], inplace=True)

print(type(dat.loc[0,'ids_niv2']))
print(dat.loc[0,'ids_niv2'])
dat.dropna(axis=0,inplace=True)
dat['ids_niv2'] = dat['ids_niv2'].astype(int)
print(dat['ids_niv2'])



datav = api.get_dataverse_contents(dat.loc[1,'ids_niv2'])
datav_ = datav.json()
print(datav_)