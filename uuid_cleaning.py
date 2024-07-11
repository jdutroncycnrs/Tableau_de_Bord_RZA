#### IMPORTATIONS ###
import re
import pandas as pd


fichier= "uuid_cat_InDoRes"

#### MAIN ####
if __name__ == "__main__":

    """with open(f"pages/data/{fichier}.txt") as file:
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
    df_uuid.to_csv(f"pages/data/{fichier}_clean.csv")"""
    
    with open(f"pages/data/{fichier}.txt") as file:
        t = file.read()
    t2 =t[70:]
    list_uuid_brutes= re.split(',', t2)
    new_list_uuid = []
    for i in range(1,len(list_uuid_brutes)):
        if "oai:search-data.ubfc.fr:" in list_uuid_brutes[i]:
            new_list_uuid.append(list_uuid_brutes[i].replace("oai:search-data.ubfc.fr:",''))
        elif "urn:isogeo:metadata:uuid:" in list_uuid_brutes[i]:
            new_list_uuid.append(list_uuid_brutes[i].replace("urn:isogeo:metadata:uuid:",''))
        else:
            try:
                new_list_uuid.append(re.split('%22', list_uuid_brutes[i])[1])
            except:
                new_list_uuid.append(list_uuid_brutes[i])
    new_list_uuid2 = []            
    for j in range(0,len(new_list_uuid)):
        try:
            new_list_uuid2.append(re.split('%22', new_list_uuid[j])[1])
        except:
            new_list_uuid2.append(new_list_uuid[j])
    df_uuid = pd.DataFrame(data= new_list_uuid2,columns=[fichier])
    df_uuid.to_csv(f"pages/data/{fichier}_clean.csv")