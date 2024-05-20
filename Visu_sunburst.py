import pandas as pd
import plotly.express as px 
import re
import numpy as np

data = pd.read_csv("liste_dataverses")
data.drop(columns=['Unnamed: 0'], inplace=True)
for i in range(len(data)):
        data.loc[i,'val']=int(len(re.split(',',data.loc[i,'Dataverses_niv2'].replace('[','').replace(']','').replace("'",''))))
print(data)

som = sum(data['val'].values)
print(som)
new_data = pd.DataFrame(index=np.arange(0,som), columns=['niv1','niv2'])
#print(new_data)

i=0
for j in range(len(data)):
    for k in range(int(data.loc[j,'val'])):
        new_data.loc[i,'niv1']=data.loc[j,'Dataverses_niv1']
        new_data.loc[i,'niv2']=re.split(',',data.loc[j,'Dataverses_niv2'].replace('[','').replace(']','').replace("'",''))[k]
        i+=1
new_data['val']=1
new_data['niv0']="Data_InDoRes"

print(new_data)
new_data.to_csv('tableau_dataverses.csv')

fig = px.sunburst(new_data, path=['niv0','niv1', 'niv2'], values='val')
fig.show()