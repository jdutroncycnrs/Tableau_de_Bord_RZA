#### IMPORTATIONS ###
import re
import pandas as pd


fichier= "uuid_cat_InDoRes"

#### MAIN ####
if __name__ == "__main__":
    with open(f"pages/data/{fichier}.txt") as file:
        t = file.read()
    list_uuid_brutes= re.split(',', t)
    new_list_uuid = []
    for i in range(len(list_uuid_brutes)):
        if "oai:search-data.ubfc.fr:" in list_uuid_brutes[i]:
            new_list_uuid.append(list_uuid_brutes[i].replace("oai:search-data.ubfc.fr:",'')[1:-1])
        elif "urn:isogeo:metadata:uuid:" in list_uuid_brutes[i]:
            new_list_uuid.append(list_uuid_brutes[i].replace("urn:isogeo:metadata:uuid:",'')[1:-1])
        else:
            try:
                new_list_uuid.append(re.split('%22', list_uuid_brutes[i])[1][1:-1])
            except:
                new_list_uuid.append(list_uuid_brutes[i][1:-1])
    df_uuid = pd.DataFrame(data= new_list_uuid,columns=[fichier])
    df_uuid.to_csv(f"pages/data/{fichier}_clean.csv")
    