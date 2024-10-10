"""import pandas as pd

liste_zam = ["info:doi:10.24396%2FORDAR-6","info:doi:10.24396%2FORDAR-5","info:doi:10.24396%2FORDAR-8","info:doi:10.24396%2FORDAR-7","info:doi:10.24396%2FORDAR-19","info:doi:10.24396%2FORDAR-112","info:doi:10.24396%2FORDAR-110","info:doi:10.24396%2FORDAR-116","info:doi:10.24396%2FORDAR-115","info:doi:10.24396%2FORDAR-114","info:doi:10.24396%2FORDAR-113","info:doi:10.24396%2FORDAR-119","info:doi:10.24396%2FORDAR-67","info:doi:10.24396%2FORDAR-128","info:doi:10.24396%2FORDAR-72","info:doi:10.24396%2FORDAR-73","info:doi:10.24396%2FORDAR-71","info:doi:10.24396%2FORDAR-76","info:doi:10.24396%2FORDAR-77","info:doi:10.24396%2FORDAR-74","info:doi:10.24396%2FORDAR-75","info:doi:10.24396%2FORDAR-78","info:doi:10.24396%2FORDAR-79","info:doi:10.24396%2FORDAR-139","info:doi:10.24396%2FORDAR-143","info:doi:10.24396%2FORDAR-148","info:doi:10.24396%2FORDAR-58","info:doi:10.24396%2FORDAR-59","info:doi:10.24396%2FORDAR-56","info:doi:10.24396%2FORDAR-62"]

df_groups = pd.read_csv("pages/data/infos_MD2/infos_groupes.csv",index_col=[0])

for i in range(len(df_groups)):
    if df_groups.loc[i,"Identifiant"] in liste_zam:
        df_groups.loc[i,"Groupe"]="zam"

df_groups.to_csv("pages/data/infos_MD2/infos_groupes.csv")

print(len(df_groups[df_groups['Groupe']=="zam"]))"""

import requests

headers_xml = {"accept":"application/xml",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}
headers_json = {"accept":"application/json",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}
identifieur = 'ead8e65d-d41c-4507-8102-dc6619ac06b6'
url = "https://cat.indores.fr/geonetwork/srv/api/records/"
url_ = url + identifieur

resp2 = requests.get(url_,headers=headers_xml)
print(resp2)
if resp2.status_code == 200:
    xml_content = resp2.text
    print(xml_content)
    try:
        print('ok')
        with open(f"{identifieur}.json", 'w') as file:
            file.write(xml_content)
    except:
        pass