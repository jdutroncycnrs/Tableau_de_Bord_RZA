import pandas as pd
import re

data = pd.read_csv("pages\data\Enregistrements_RZA_060524.csv")
data.rename(columns={"createDate":"Date"}, inplace=True)

data_recordOwner = data['uuid']
data_recordOwner.dropna(inplace=True)
n = len(data_recordOwner)

print(n)


"""data_thematiques = data['cl_topic']
liste_thema = []
for i in range(len(data)):
    try:
        l = re.split(',',data.loc[i,'cl_topic'][1:-1])
        for j in range(len(l)):
            liste_thema.append(l[j].strip().replace("'",'').strip())
    except:
        pass
for i in range(len(liste_thema)):
    if liste_thema[i]=='environmen':
        liste_thema[i]='environnement'
    if liste_thema[i]=='environment':
        liste_thema[i]='environnement'
    if liste_thema[i]=='climatology':
        liste_thema[i]='climatologie'
set_thematiques = set(liste_thema)

st.write(set_thematiques)
st.write(len(set_thematiques))
st.write(data.loc[0,'cl_topic'][0])

cnt_thematiques = data_thematiques.value_counts()
df_thematiques = pd.DataFrame(cnt_thematiques.values, index=cnt_thematiques.index.values,columns=['compte_thema'])
st.subheader(f'Thématiques')
st.write(len(cnt_thematiques))
st.table(cnt_thematiques)
st.bar_chart(df_thematiques)"""