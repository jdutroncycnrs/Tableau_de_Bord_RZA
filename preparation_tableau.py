import pandas as pd
from datetime import datetime
import numpy as np
import re

def prepa_date(tableau, rule="6ME"):
    tableau_date = tableau.copy()
    tableau_date.set_index('Date', inplace=True)
    tableau_date_resampled = tableau_date.resample(rule=rule).size()
    liste_dates = tableau_date_resampled.index.values
    liste_comptes = tableau_date_resampled.values
    df_date = pd.DataFrame([liste_dates,liste_comptes], index=['Date','Compte_resampled']).T
    df_date['Date'] = pd.to_datetime(df_date['Date'], format='mixed', utc=True)
    return df_date

def year(tableau):
    tableau_year = tableau.copy()
    tableau_year['Date'] = pd.to_datetime(tableau_year['Date'], format='mixed', utc=True)
    tableau_year.sort_values(by="Date", inplace=True)
    tableau_year.reset_index(inplace=True)
    tableau_year.drop(columns='index',inplace=True)
    for i in range(len(tableau_year)):
        try:
            y = datetime.date(tableau_year.loc[i,'Date']).year
            if y==1:
                y=np.NaN
        except:
            y = np.NAN
        tableau_year.loc[i,'Year']= y
    return tableau_year

def coordonnees(tableau):
    tableau_coord = tableau.copy()
    tableau_coord['lat']=(tableau_coord['Latitude_Sud']+tableau_coord['Latitude_Nord'])/2
    tableau_coord['long']=(tableau_coord['Longitude_Ouest']+tableau_coord['Longitude_Est'])/2
    return tableau_coord

def remove_duplicate_patterns(text,pattern):
        occurrences = list(re.finditer(pattern, text))
    
        if not occurrences:
            return text  

        for match in occurrences[1:]:
            text = text[:match.start()] + text[match.end():]
        
        return text

def traitement_thesaurus(tableau):
    tableau_ = tableau.copy()
    tableau_.reset_index(inplace=True)
    tableau_.drop(columns='index',inplace=True)
    for i in range(len(tableau_)):
        tableau_.loc[i,'Thesaurus']=tableau_.loc[i,'Thesaurus'][1:-1]
        if len(tableau_.loc[i,'Thesaurus'])==0:
            tableau_.loc[i,'Thesaurus_usage']="NON"
        else:
            tableau_.loc[i,'Thesaurus_usage']="OUI"

    tableau_oui = tableau_[tableau_['Thesaurus_usage']=='OUI']
    tableau_oui.reset_index(inplace=True)
    tableau_oui.drop(columns='index',inplace=True)
    tableau_non = tableau_[tableau_['Thesaurus_usage']=='NON']
    tableau_non.reset_index(inplace=True)
    tableau_non.drop(columns='index',inplace=True)

    def transfo(x):
        return [item.strip().strip("'") for item in x.split(',')]

    tableau_oui['Thesaurus_listed'] = tableau_oui['Thesaurus'].apply(transfo)
    tableau_oui['Thesaurus_listed_len'] = tableau_oui['Thesaurus_listed'].apply(lambda x:len(x))

    elements_to_remove = {'version 1.0', 'version 2.4'}
    tableau_oui['Thesaurus_listed'] = tableau_oui['Thesaurus_listed'].apply(lambda lst: [x for x in lst if x not in elements_to_remove])
    pattern = 'GEMET - INSPIRE themes'
    pattern2 = 'Continents countries sea regions of the world'
    pattern3 = 'Régions administratives de France'
    replace_dict = {'INSPIRE themes': pattern,
                    'GEMET':pattern,
                    'Registre de thème INSPIRE':pattern,
                    'GEMET inspire themes - version 1.0':pattern,
                    'GEMET Thesaurus version 1.0':pattern,
                    'INSPIRE':pattern,
                    'inspire':pattern,
                    'Gemet':pattern,
                    'Continents':pattern2,
                    'countries':pattern2,
                    'sea regions of the world':pattern2,
                    'sea regions of the world.':pattern2,
                    'Region':pattern3}
    tableau_oui['Thesaurus_listed'] = tableau_oui['Thesaurus_listed'].apply(lambda lst: [replace_dict.get(x, x) for x in lst])
    tableau_oui['Thesaurus_listed'] = tableau_oui['Thesaurus_listed'].apply(set)
    tableau_oui['Thesaurus_listed'] = tableau_oui['Thesaurus_listed'].apply(list)

    return tableau_ ,tableau_oui, tableau_non

def traitement_mots_cles(tableau):
    tableau_ = tableau.copy()
    tableau_.reset_index(inplace=True)
    tableau_.drop(columns='index',inplace=True)
    for i in range(len(tableau_)):
        tableau_.loc[i,'Mots_clés']=tableau_.loc[i,'Mots_clés'][1:-1]
        tableau_.loc[i,'Mots_clés']=tableau_.loc[i,'Mots_clés'].replace(';',',')

    def transfo(x):
        return [item.strip().strip("'") for item in x.split(',')]
    
    tableau_['Mots_clés_listed'] = tableau_['Mots_clés'].apply(transfo)
    tableau_['Mots_clés_listed_len'] = tableau_['Mots_clés_listed'].apply(lambda x:len(x))

    return tableau_