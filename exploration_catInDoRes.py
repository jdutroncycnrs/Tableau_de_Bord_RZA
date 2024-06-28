########### IMPORTATION ##############
import requests
import pandas as pd
import json
import xmltodict

fichier_uuids = "data/uuid_cat_InDoRes_clean_compared.csv"

######################## URL de l'API ##############################
url = "https://cat.indores.fr/geonetwork/srv/api/records/"
####################################################################

headers = {"accept":"application/json",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}

### Récupération des variables choisies dans les fiches du GN ######


if __name__=="__main__":

    uuids = pd.read_csv(fichier_uuids, index_col=[0])
    i = uuids.loc[0,'uuid_cat_InDoRes'].replace('"','')
    url_ = url + i
    resp = requests.get(url_,headers=headers)
    st=resp.json()

    test = {}
    test["gmd:MD_Metadata"]=st

    with open(f"data/{i}.json", "w") as f:
        json.dump(test, f, indent=4)

    ############# VERS XML
    with open(f"data/{i}.json","r") as file:
        python_dict=json.load(file)
    
    # Convert the JSON data to XML 
    xml_data = xmltodict.unparse(python_dict,pretty=True)

    with open(f"data/{i}.xml","w") as xml_file:
        xml_file.write(xml_data)
        xml_file.close()