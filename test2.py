import pandas as pd
import re

data = pd.read_csv("pages/data/Enregistrements_RZA_030524.csv")
data.rename(columns={"createDate":"Date"}, inplace=True)
data.drop(columns=['any.langfre'], inplace=True)

liste_columns_data = data.columns.values
for c in liste_columns_data:
    for i in range(len(data)):
        l = data.loc[i,c]
        data.loc[i,c] = re.split(',',l)

data.to_csv('data')

data2 = pd.read_csv('data')
data2.drop(columns=['Unnamed: 0'], inplace=True)

liste_index= data2.index.values
liste_columns_data2 = data2.columns.values
data_bis = pd.DataFrame(index=liste_index,columns=['ZAA','ZAAJ','ZAAR','ZAEU','ZAS','ZAM','ZABRI','ZABR','ZAL','ZAPygar'])

rechercheZAA = ['ZAA', 'Zone Atelier Alpes']
rechercheZAAJ = ['ZAAJ', 'Zone Atelier Arc Jurassien']
rechercheZAAR = ['ZAAR', 'Zone Atelier Armorique']
rechercheZAEU = ['ZAEU', 'Zone Atelier Environnementale Urbaine']
rechercheZAS = ['ZAS','Zone Atelier Seine']
rechercheZAM = ['ZAM', 'Zone Atelier Moselle']
rechercheZABRI = ['ZABRI','Zone Atelier Brest Iroise']
rechercheZABR = ['ZABR','Zone Atelier Bassin du Rhone']
rechercheZAL = ['ZAL','Zone Atelier Loire']
rechercheZAPygar = ['ZAPygar', 'Zone Atelier Pyrénées Garonne' ]

for c in liste_columns_data2:
    for i in range(len(data2)):
        lis = data2.loc[i,c]
        for u in rechercheZAA:
            if u in lis:
                data_bis.loc[i,'ZAA']=1
            else:
                pass
        for u in rechercheZAAJ:
            if u in lis:
                data_bis.loc[i,'ZAAJ']=1
            else:
                pass
        for u in rechercheZAAR:
            if u in lis:
                data_bis.loc[i,'ZAAR']=1
            else:
                pass
        for u in rechercheZAEU:
            if u in lis:
                data_bis.loc[i,'ZAEU']=1
            else:
                pass
        for u in rechercheZAS:
            if u in lis:
                data_bis.loc[i,'ZAS']=1
            else:
                pass
        for u in rechercheZAM:
            if u in lis:
                data_bis.loc[i,'ZAM']=1
            else:
                pass
        for u in rechercheZABRI:
            if u in lis:
                data_bis.loc[i,'ZABRI']=1
            else:
                pass
        for u in rechercheZABR:
            if u in lis:
                data_bis.loc[i,'ZABR']=1
            else:
                pass
        for u in rechercheZAL:
            if u in lis:
                data_bis.loc[i,'ZAL']=1
            else:
                pass
        for u in rechercheZAPygar:
            if u in lis:
                data_bis.loc[i,'ZAPygar']=1
            else:
                pass

data_bis.to_csv('data_bis')

print('ZAA:',len(data_bis['ZAA'][data_bis['ZAA']==1]))
print('ZAAJ:',len(data_bis['ZAAJ'][data_bis['ZAAJ']==1]))
print('ZAAR:',len(data_bis['ZAAR'][data_bis['ZAAR']==1]))
print('ZAEU:',len(data_bis['ZAEU'][data_bis['ZAEU']==1]))
print('ZAM:',len(data_bis['ZAM'][data_bis['ZAM']==1]))
print('ZAS:',len(data_bis['ZAS'][data_bis['ZAS']==1]))
print('ZABRI:',len(data_bis['ZABRI'][data_bis['ZABRI']==1]))
print('ZABR:',len(data_bis['ZABR'][data_bis['ZABR']==1]))
print('ZAL:',len(data_bis['ZAL'][data_bis['ZAL']==1]))
print('ZAPygar:',len(data_bis['ZAPygar'][data_bis['ZAPygar']==1]))
