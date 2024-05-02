import pandas as pd
import re

data = pd.read_csv("pages/data/Enregistrements_RZA_020524.csv")
data.rename(columns={"createDate":"Date"}, inplace=True)