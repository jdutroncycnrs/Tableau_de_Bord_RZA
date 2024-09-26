"""import pandas as pd

liste_zam = ["info:doi:10.24396%2FORDAR-6","info:doi:10.24396%2FORDAR-5","info:doi:10.24396%2FORDAR-8","info:doi:10.24396%2FORDAR-7","info:doi:10.24396%2FORDAR-19","info:doi:10.24396%2FORDAR-112","info:doi:10.24396%2FORDAR-110","info:doi:10.24396%2FORDAR-116","info:doi:10.24396%2FORDAR-115","info:doi:10.24396%2FORDAR-114","info:doi:10.24396%2FORDAR-113","info:doi:10.24396%2FORDAR-119","info:doi:10.24396%2FORDAR-67","info:doi:10.24396%2FORDAR-128","info:doi:10.24396%2FORDAR-72","info:doi:10.24396%2FORDAR-73","info:doi:10.24396%2FORDAR-71","info:doi:10.24396%2FORDAR-76","info:doi:10.24396%2FORDAR-77","info:doi:10.24396%2FORDAR-74","info:doi:10.24396%2FORDAR-75","info:doi:10.24396%2FORDAR-78","info:doi:10.24396%2FORDAR-79","info:doi:10.24396%2FORDAR-139","info:doi:10.24396%2FORDAR-143","info:doi:10.24396%2FORDAR-148","info:doi:10.24396%2FORDAR-58","info:doi:10.24396%2FORDAR-59","info:doi:10.24396%2FORDAR-56","info:doi:10.24396%2FORDAR-62"]

df_groups = pd.read_csv("pages/data/infos_MD2/infos_groupes.csv",index_col=[0])

for i in range(len(df_groups)):
    if df_groups.loc[i,"Identifiant"] in liste_zam:
        df_groups.loc[i,"Groupe"]="zam"

df_groups.to_csv("pages/data/infos_MD2/infos_groupes.csv")

print(len(df_groups[df_groups['Groupe']=="zam"]))"""