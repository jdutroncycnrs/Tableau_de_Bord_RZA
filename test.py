import pandas as pd
import re


data = pd.read_csv("pages/data/Enregistrements_RZA_020524.csv")
data.rename(columns={"createDate":"Date"}, inplace=True)



dico = {'Jan':'01',
        'Feb':'02',
        'Mar':'03',
        'Apr':'04',
        'May':'05',
        'Jun':'06',
        'Jul':'07',
        'Aug':'08',
        'Sep':'09',
        'Oct':'10',
        'Nov':'11',
        'Dec':'12'}
dico2 = {' 1,':' 01',
         ' 2,':' 02',
         ' 3,':' 03',
         ' 4,':' 04',
         ' 5,':' 05',
         ' 6,':' 06',
         ' 7,':' 07',
         ' 8,':' 08',
         ' 4,':' 09'}
for i in range(len(data)):
    for term, num in dico.items():
        data.loc[i,'Date'] = data.loc[i,'Date'].replace(term,num).replace('@','/')
    for term, num in dico2.items():
        data.loc[i,'Date'] = data.loc[i,'Date'].replace(term,num).replace(',','')
    data.loc[i,'Date'] = re.split('/',data.loc[i,'Date'])[0][0:-1].replace(' ','-')+re.split('/',data.loc[i,'Date'])[1]

data['Date'] = pd.to_datetime(data['Date'], format='%m-%d-%Y %H:%M:%S.%f', utc=True)
print(data['Date'][0])