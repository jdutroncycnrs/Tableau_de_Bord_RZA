import pandas as pd
import re

data = pd.read_csv("pages\data\Enregistrements_RZA_060524.csv")
data.rename(columns={"createDate":"Date"}, inplace=True)

data_format = data['format']
cnt = data_format.value_counts()
print(cnt)