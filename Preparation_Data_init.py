import pandas as pd
import numpy as np
from datetime import datetime
import re
import missingno as msno
import seaborn as sns
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None

fichier = 'Enregistrements_RZA_020624'
data = pd.read_csv(f"pages/data/{fichier}.csv")


data_columns = data.columns.values
liste_col_link = []
for i,x in enumerate(data_columns):
    if 'link' in data_columns[i]:
        liste_col_link.append(x)

data_link = data[liste_col_link]
l=['linkUrlProtocolDOI','linkUrl','linkProtocol','linkUrlProtocol','linkUrlProtocoldoi',
   'linkUrlProtocolESRIArcGIShttpconfiguration','linkUrlProtocolnull','linkUrlProtocolOGCEDR',
   'linkUrlProtocolOGCWCS','linkUrlProtocolOGCWFS','linkUrlProtocolOGCWFS100httpgetcapabilities',
   'linkUrlProtocolOGCWMS','linkUrlProtocolOGCWMS111httpgetmap','linkUrlProtocolUKST',
   'linkUrlProtocolWWWDOWNLOAD','linkUrlProtocolWWWDOWNLOAD10ftpdownload','linkUrlProtocolWWWDOWNLOAD10httpdownload',
   'linkUrlProtocolWWWLINK','linkUrlProtocolWWWLINK10httplink','linkUrlProtocolWWWLINK10httppartners']

data_link['test']= data_link[l[0]]
for col in l[1:]:
    data_link['test2'] = data_link['test'] + data_link[col]
    data_link['test'] = data_link['test2']

for i in range(len(data_link)):
    data_link.loc[i,'test']=str(data_link.loc[i,'test']).replace('-','').strip()

print(data_link.loc[2,'test'])
print(type(data_link.loc[2,'test']))
print(data_link['test'].head())

for i in range(len(data_link)):
    if "doi" in str(data_link.loc[i,'test']):
        data_link.loc[i,'DOI']=1
    else:
        data_link.loc[i,'DOI']=0
print(data_link['DOI'].head())
print(len(data))
print(len(data_link[data_link['DOI']==0.0]))

plt.figure(figsize=(5,5))
sns.heatmap(data_link[['DOI']]==0.0, cbar=False)
plt.show()