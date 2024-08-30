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

def traitement_langues(tableau):
    tableau_ = tableau.copy()

    for i in range(len(tableau_)):
            if tableau_.loc[i,'Langue']=="['en' 'fr']":
                tableau_.loc[i,'Langue']="eng & fre"
            elif tableau_.loc[i,'Langue']=="en":
                tableau_.loc[i,'Langue']="eng"
            elif tableau_.loc[i,'Langue']=="ang":
                tableau_.loc[i,'Langue']="eng"
            elif tableau_.loc[i,'Langue']=="['fr']":
                tableau_.loc[i,'Langue']="fre"
    
    return tableau_

def traitement_standards(tableau):
    tableau_ = tableau.copy()

    for i in range(len(tableau_)):
            if tableau_.loc[i,'Standard']=="ISO 19115:2003 Geographic information - Metadata":
                tableau_.loc[i,'Standard']="ISO 19115:2003/19139"
            elif tableau_.loc[i,'Standard']=="ISO 19115-2 Geographic Information - Metadata Part 2 Extensions for imagery and gridded data":
                tableau_.loc[i,'Standard']="ISO 19115-2 Extensions for imagery and gridded data"
            elif tableau_.loc[i,'Standard']=="ISO 19115/19139":
                tableau_.loc[i,'Standard']="ISO 19115:2003/19139"
            elif tableau_.loc[i,'Standard']=="http://www.isotc211.org/2005/gco":
                tableau_.loc[i,'Standard']="ISO 19136:2005"
            elif tableau_.loc[i,'Standard']=="https://cat.indores.fr/geonetwork/xml/schemas/dublin-core/schema.xsd":
                tableau_.loc[i,'Standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Standard']=="Cendrine":
                tableau_.loc[i,'Standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Standard']=="patricia cicille":
                tableau_.loc[i,'Standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Standard']=="07170":
                tableau_.loc[i,'Standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Standard']=="23, rue Jean Baldassini":
                tableau_.loc[i,'Standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Standard']=="UK GEMINI":
                tableau_.loc[i,'Standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Standard']=="Chenouf Sarra":
                tableau_.loc[i,'Standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Standard']=="ISO 19115-3 ISO 19115-3":
                tableau_.loc[i,'Standard']="ISO 19115-3"
            elif tableau_.loc[i,'Standard']=="ISO19139":
                tableau_.loc[i,'Standard']="ISO 19115:2003/19139"
    
    return tableau_

def traitement_formats(tableau):
    tableau_ = tableau.copy()
    for i in range(len(tableau_)):
        try:
            tableau_.loc[i,'Format']=tableau_.loc[i,'Format'][2:-2]
        except:
            pass
        if tableau_.loc[i,'Format']=='':
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="Pas de logiciel associé à la donnée":
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="modèle de simulation du Grand Lyon":
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="Vigilance":
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="inapplicable":
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="application/pdf":
            tableau_.loc[i,'Format']="PDF"
        elif tableau_.loc[i,'Format']=="application/x-shapefile":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="esri Shapefile":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="Esri Shapefile":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="SHP":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="GeoTiff":
            tableau_.loc[i,'Format']="GeoTIFF"
        elif tableau_.loc[i,'Format']=="GEOTIFF":
            tableau_.loc[i,'Format']="GeoTIFF"
        elif tableau_.loc[i,'Format']=="TIFF":
            tableau_.loc[i,'Format']="GeoTIFF"
        elif tableau_.loc[i,'Format']=="TIF":
            tableau_.loc[i,'Format']="GeoTIFF"
        elif tableau_.loc[i,'Format']=="shape":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="EXCEL":
            tableau_.loc[i,'Format']="XLS"
        elif tableau_.loc[i,'Format']=="application/vnd.ms-excel":
            tableau_.loc[i,'Format']="XLS"
        elif tableau_.loc[i,'Format']=="application/vnd.ms-excel' 'text/csv":
            tableau_.loc[i,'Format']="XLS"
        elif tableau_.loc[i,'Format']=="application/pdf' 'application/vnd.ms-excel":
            tableau_.loc[i,'Format']="PDF"
        elif tableau_.loc[i,'Format']=="Jpeg2000":
            tableau_.loc[i,'Format']="JPEG"
        elif tableau_.loc[i,'Format']=="IRB, TIF, JPEG, BMP":
            tableau_.loc[i,'Format']="JPEG"
        elif tableau_.loc[i,'Format']=="Mammouth":
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="text/csv":
            tableau_.loc[i,'Format']="TXT"
        elif tableau_.loc[i,'Format']=="GDB":
            tableau_.loc[i,'Format']="ESRI Shapefile"

    return tableau_

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