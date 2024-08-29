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
    pattern = "'GEMET_INSPIRE_themes_V1'"
    pattern2 = "'GEMET_INSPIRE_concepts_V2.4'"
    pattern3 = "'GEMET_INSPIRE_concepts_V4.1.4'"
    pattern4 = "'Continents_Countries_Seas'"
    'GEMET_INSPIRE_themes_V1', 
    for i in range(len(tableau)):
        tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'][1:-1]
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'GEMET - INSPIRE themes, version 1.0'", pattern)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace(" 'GEMET_INSPIRE_themes_V1'", pattern)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'GEMET_INSPIRE_themes_V1' ", pattern)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'GEMET_INSPIRE_themes_V1', ", pattern)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'GEMET inspire themes - version 1.0'", pattern)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'INSPIRE themes'", pattern)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'INSPIRE'", pattern)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'GEMET'", pattern)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'Registre de thème INSPIRE'", pattern)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'GEMET - Concepts, version_2.4'", pattern2)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'GEMET - Concepts, version 4.1.4", pattern3)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'Continents, countries, sea regions of the world.'", pattern4)
        except:
            pass
        try:
            tableau.loc[i,'Thesaurus']=tableau.loc[i,'Thesaurus'].replace("'Continents, countries, sea regions of the world'", pattern4)
        except:
            pass

        tableau.loc[i,'Thesaurus']=remove_duplicate_patterns(tableau.loc[i,'Thesaurus'],pattern)
        tableau.loc[i,'Thesaurus'] = tableau.loc[i,'Thesaurus'].replace("  ","")

    thesaurus_existants = []
    for i in range(len(tableau)):
        l = re.split(",",tableau.loc[i,'Thesaurus'])
        for j in range(len(l)):
            thesaurus_existants.append(l[j])
    
    thesaurus_existants_set = set(thesaurus_existants)
    return tableau, thesaurus_existants_set


def traitement_thesaurus_(tableau):

    pattern = "GEMET_INSPIRE_themes_V1"
    pattern2 = "theme.thesaurus_costel.rdf"
    pattern3 = "theme.EnvironnementFR.rdf"
    pattern4 = "Vocabulaire MétaZABR"
    pattern5 = "Régions administratives de France"
    pattern6 = "GEMET - Conceptsversion 2.4"
    pattern7 = "Continents,countries,sea regions of the world."
    pattern8 = "Nouvelles Régions de France"

    liste_patterns = [pattern,pattern2,pattern3,pattern4,pattern5,pattern6,pattern7, pattern8]

    
    
    for i in range(len(tableau)):
        tableau.loc[i,'Thesaurus'] = tableau.loc[i,'Thesaurus'].replace("'","").strip()
        
    #for i in range(len(tableau)):    
        #if len(tableau.loc[i,'Thesaurus'])==1 and tableau.loc[i,'Thesaurus'][0] =='':
            #tableau.loc[i,'Thesaurus_usage']='NON'
        #else:
            #tableau.loc[i,'Thesaurus_usage']='OUI'

    return tableau