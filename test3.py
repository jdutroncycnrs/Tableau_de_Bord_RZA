import pandas as pd

data = pd.read_csv("pages/data/Enregistrements_RZA_220524_ready.csv")
print(data['Datestamp'])