import pandas as pd
import requests
import json
import re
import streamlit as st

def transcript_json(json_data, file, prefix=""):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, dict) or isinstance(value, list):
                transcript_json(value,file, f"{prefix}.{key}" if prefix else key)
            else:
                #print(f"{prefix}.{key}: {value}" if prefix else f"{key}: {value}")
                file.write(f"{prefix}.{key}:§{value}µ" if prefix else f"{key}:§{value}µ")
    elif isinstance(json_data, list):
        for item in json_data:
            transcript_json(item,file, prefix)
    else:
        #print(f"{prefix}: {json_data}" if prefix else f"{json_data}")
        file.write(f"{prefix}:§{json_data}µ" if prefix else f"{json_data}µ")


def recup_themes_thesaurus_motsCles(url, identifieur, headers_json):
    url_ = url + identifieur
    resp1 = requests.get(url_,headers=headers_json)
    if resp1.status_code == 200:
        resp_json=resp1.json()
        if "oai:search-data.ubfc.fr" in identifieur:
            identifieur = identifieur.replace('oai:search-data.ubfc.fr:','zaaj_')
            with open(f"pages/data/fiches_json2/{identifieur}.json", "w") as f:
                json.dump(resp_json, f)
        else:
            with open(f"pages/data/fiches_json2/{identifieur}.json", "w") as f:
                json.dump(resp_json, f)

        with open(f"pages/data/fiches_json2/{identifieur}.json", 'r') as f2:
            data = json.load(f2)

        with open(f'pages/data/fiches_txt2/{identifieur}.txt', 'w') as file:
            transcript_json(data, file)

        with open(f'pages/data/fiches_txt2/{identifieur}.txt', 'r') as f:
            d = f.read()

        listi = re.split('µ',d)

        df = pd.DataFrame(listi, columns=['Results'])
        for u in range(len(df)):
            p = re.split('§',df.loc[u,'Results'])
            try:
                df.loc[u,'Valeurs']=p[1]
            except:
                pass
            try:
                df.loc[u,'Clés']=p[0].replace('.','£')
            except:
                pass

        for j in range(len(df)):
            pp = re.split('£',df.loc[j,'Clés'])
            for k in range(15):
                try:
                    df.loc[j,f'K{k}']=pp[k]
                except:
                    pass

        Liste_Theme = []
        Liste_Thesaurus = []
        Mots_cles = []
        Mots_cles_zaaj = []
        if 'zaaj_' in identifieur: 
            try:
                for u in range(len(df)):
                    if df.loc[u,'Clés']=="dc:subject£#text:":
                        Mots_cles_zaaj.append(df.loc[u,'Valeurs'])
            except:
                pass
        else:
            try:
                for u in range(len(df)):
                    if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:type£gmd:MD_KeywordTypeCode£@codeListValue:":
                        Liste_Theme.append([u,df.loc[u,'Valeurs']])
            except:
                pass
            try:
                for u in range(len(df)):
                    if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:thesaurusName£gmd:CI_Citation£gmd:title£gco:CharacterString£#text:":
                        Liste_Thesaurus.append([u,df.loc[u,'Valeurs']])
            except:
                pass
            try:
                for u in range(len(df)):
                    if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:keyword£gco:CharacterString£#text:" or  df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:keyword£gmx:Anchor£#text:":
                        Mots_cles.append([u,df.loc[u,'Valeurs']])
            except:
                pass

        theme_thesaurus_motsCles = []
        mm = 0    
        for th in range(1):
            liste_mots_cles = []
            try:
                if Liste_Theme[th][0]< Liste_Thesaurus[th][0]:
                    for m in range(mm,len(Mots_cles)):
                        if Mots_cles[m][0]<Liste_Theme[th][0]:
                            liste_mots_cles.append(Mots_cles[m][1])
                            mm = m
                    theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],Liste_Thesaurus[th][1]])
            except:
                try:
                    for m in range(mm,len(Mots_cles)):
                        if Mots_cles[m][0]<Liste_Theme[th][0]:
                            liste_mots_cles.append(Mots_cles[m][1])
                            mm = m
                    theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],"Aucun thésaurus"])
                except:
                    theme_thesaurus_motsCles.append([liste_mots_cles,"Aucun thème","Aucun thésaurus"])

        for th in range(1,len(Liste_Theme)):
            liste_mots_cles = []
            try:
                if Liste_Theme[th][0]< Liste_Thesaurus[th][0]:
                    for m in range(mm+1,len(Mots_cles)):
                        if Mots_cles[m][0]<Liste_Theme[th][0]:
                            liste_mots_cles.append(Mots_cles[m][1])
                            mm = m
                    theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],Liste_Thesaurus[th][1]])
            except:
                try:
                    for m in range(mm+1,len(Mots_cles)):
                        if Mots_cles[m][0]<Liste_Theme[th][0]:
                            liste_mots_cles.append(Mots_cles[m][1])
                            mm = m
                    theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],"Aucun thésaurus"])
                except:
                    theme_thesaurus_motsCles.append([liste_mots_cles,"Aucun thème","Aucun thésaurus"])

    return theme_thesaurus_motsCles


def recup_fiche2(url, identifieur, headers_json, filtre_mention):
    url_ = url + identifieur
    resp1 = requests.get(url_,headers=headers_json)
    if resp1.status_code == 200:
        resp_json=resp1.json()
        if "oai:search-data.ubfc.fr" in identifieur:
            identifieur = identifieur.replace('oai:search-data.ubfc.fr:','zaaj_')
            with open(f"pages/data/fiches_json2/{identifieur}.json", "w") as f:
                json.dump(resp_json, f)
        else:
            with open(f"pages/data/fiches_json2/{identifieur}.json", "w") as f:
                json.dump(resp_json, f)

        with open(f"pages/data/fiches_json2/{identifieur}.json", 'r') as f2:
            data = json.load(f2)

        with open(f'pages/data/fiches_txt2/{identifieur}.txt', 'w') as file:
            transcript_json(data, file)

        with open(f'pages/data/fiches_txt2/{identifieur}.txt', 'r') as f:
            d = f.read()

        listi = re.split('µ',d)

        df = pd.DataFrame(listi, columns=['Results'])
        for u in range(len(df)):
            p = re.split('§',df.loc[u,'Results'])
            try:
                df.loc[u,'Valeurs']=p[1]
            except:
                pass
            try:
                df.loc[u,'Clés']=p[0].replace('.','£')
            except:
                pass

        for j in range(len(df)):
            pp = re.split('£',df.loc[j,'Clés'])
            for k in range(15):
                try:
                    df.loc[j,f'K{k}']=pp[k]
                except:
                    pass
        df.to_csv(f'pages/data/fiches_csv2/{identifieur}.csv')

        if "zaaj_" in identifieur:
                try:
                    Langue = df['Valeurs'][df['Clés']=="dc:title£@xml:lang:"].values
                except:
                    Langue = ""
        else:
            try:
                Langue = df['Valeurs'][df['Clés']=="gmd:language£gco:CharacterString£#text:"].values[0]
            except:
                try:
                    Langue = df['Valeurs'][df['Clés']=="gmd:language£gmd:LanguageCode£@codeListValue:"].values[0]
                except:
                    Langue = ""
        try:
            JeuDeCaracteres = df['Valeurs'][df['Clés']=="gmd:characterSet£gmd:MD_CharacterSetCode£@codeListValue:"].values[0]
        except:
            JeuDeCaracteres =""
        try:
            Type = df['Valeurs'][df['Clés']=="gmd:hierarchyLevel£gmd:MD_ScopeCode£@codeListValue:"].values[0]
        except:
            try:
                Type = df['Valeurs'][df['Clés']=="gfc:featureType£gfc:FC_FeatureType£gfc:typeName£gco:LocalName£#text:"].values[0]
            except:
                try:
                    Type = df['Valeurs'][df['Clés']=="dc:type£#text:"].values[0]
                except:
                    Type =""
        try:
            Date = df['Valeurs'][df['Clés']=="gmd:dateStamp£gco:DateTime£#text:"].values[0]
        except:
            try:
                Date = df['Valeurs'][df['Clés']=="gfc:versionDate£gco:DateTime£#text:"].values[0]
            except:
                try:
                    Date = df['Valeurs'][df['Clés']=="gmx:versionDate£gco:DateTime£#text:"].values[0]
                except:
                    try:
                        Date = df['Valeurs'][df['Clés']=="dc:date£#text:"].values[0]
                    except:
                        Date = ""

        if 'zaaj_' in identifieur:  
            try:                      
                Standard = df['Valeurs'][df['Clés']=="@xsi:noNamespaceSchemaLocation:"].values[0]
            except:
                    Standard = ""
        else:
            try:
                Standard = df['Valeurs'][df['Clés']=="gmd:metadataStandardName£gco:CharacterString£#text:"].values[0]
            except:
                try:
                    Standard = df['Valeurs'][df['Clés']=="gfc:name£gco:CharacterString£@xmlns:gco:"].values[0]
                except:
                    Standard = ""
        try:
            Version_standard = df['Valeurs'][df['Clés']=="gmd:metadataStandardVersion£gco:CharacterString£#text:"].values[0]
        except:
            Version_standard = ""

        if 'zaaj_' in identifieur:    
            try:                    
                Nom_contact = df['Valeurs'][df['Clés']=="dc:creator£#text:"].values
            except:
                Nom_contact = ""
        else:
            try:
                Nom_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values
                if len(Nom_contact)==0:
                    Nom_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values
            except:
                try:
                    Nom_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values
                except:
                    try:
                        Nom_contact = df['Valeurs'][df['Clés']=="gfc:producer£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values[0]
                    except: 
                        Nom_contact = ""

        if 'zaaj_' in identifieur:  
            try:                      
                Organisation_contact = df['Valeurs'][df['Clés']=="dc:publisher£#text:"].values
            except:
                Organisation_contact = ""
        else:
            try:
                Organisation_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values
                if len(Organisation_contact)==0:
                    Organisation_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values
            except:
                try:
                    Organisation_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values
                except:
                    Organisation_contact = ""
        try:
            Position_contact =df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values
            if len(Position_contact)==0:
                Position_contact =df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values
        except:
            try:
                Position_contact =df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values
            except:
                Position_contact = ""
        try:
            Tel_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values
            if len(Tel_contact)==0:
                Tel_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values
        except:
            try:
                Tel_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values
            except:
                Tel_contact = ""
        try:
            DeliveryPoint = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:deliveryPoint£gco:CharacterString£#text:"].values
            if len(DeliveryPoint)==0:
                DeliveryPoint = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:deliveryPoint£gco:CharacterString£#text:"].values
        except:
            try:
                DeliveryPoint = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:deliveryPoint£gco:CharacterString£#text:"].values
            except:
                DeliveryPoint = ""
        try:
            CodePostal = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:postalCode£gco:CharacterString£#text:"].values
            if len(CodePostal)==0:
                CodePostal = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:postalCode£gco:CharacterString£#text:"].values
        except:
            try:
                CodePostal = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:postalCode£gco:CharacterString£#text:"].values
            except:
                CodePostal = ""
        try:
            Ville = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:city£gco:CharacterString£#text:"].values
            if len(Ville)==0:
                Ville = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:city£gco:CharacterString£#text:"].values
        except:
            try:
                Ville = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:city£gco:CharacterString£#text:"].values
            except:
                Ville = ""
        try:
            Pays = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:country£gco:CharacterString£#text:"].values
            if len(Pays)==0:
                Pays = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:country£gco:CharacterString£#text:"].values
        except:
            try:
                Pays = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:country£gco:CharacterString£#text:"].values
            except:
                Pays =""
        try:
            Email = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:electronicMailAddress£gco:CharacterString£#text:"].values[0]
        except:
            try:
                Email = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:electronicMailAddress£gco:CharacterString£#text:"].values[0]
            except:
                Email = ""


        try:
            SystemReference =  df['Valeurs'][df['Clés']=="gmd:referenceSystemInfo£gmd:MD_ReferenceSystem£gmd:referenceSystemIdentifier£gmd:RS_Identifier£gmd:code£gco:CharacterString£#text:"].values
        except:
            SystemReference = ""
        try:
            westBoundLongitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:westBoundLongitude£gco:Decimal£#text:"].values[0]
        except:
            westBoundLongitude = ""
        try:
            EastBoundLongitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:eastBoundLongitude£gco:Decimal£#text:"].values[0]
        except:
            EastBoundLongitude = ""
        try:
            SouthBoundLatitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:southBoundLatitude£gco:Decimal£#text:"].values[0]
        except:
            SouthBoundLatitude = ""
        try:
            NorthBoundLatitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:northBoundLatitude£gco:Decimal£#text:"].values[0]
        except:
            NorthBoundLatitude = ""

        try: 
            Titre = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:title£gco:CharacterString£#text:"].values[0]
        except:
            try:
                Titre = df['Valeurs'][df['Clés']=="gfc:name£gco:CharacterString£#text:"].values[0]
            except:
                try:
                    Titre = df['Valeurs'][df['Clés']=="dc:title£#text:"].values[0]
                except:
                    Titre = ""
        try: 
            FicheParent = df['Valeurs'][df['Clés']=="gmd:parentIdentifier£gco:CharacterString£#text:"].values[0]
        except:
            FicheParent = ""

        if 'zaaj_' in identifieur:
            try:
                Abstract =df['Valeurs'][df['Clés']=="dc:description£#text:"].values
            except:
                Abstract = ""
        else:
            try:
                Abstract =df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:abstract£gco:CharacterString£#text:"].values[0]
            except:
                Abstract = ""

        try:
            Date_creation = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:date£gco:DateTime£#text:"].values[0]
        except:
            Date_creation = ""
        try:
            Purpose = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:purpose£gco:CharacterString£#text:"].values[0]
        except:
            Purpose = ""
        try:
            Status = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:status£gmd:MD_ProgressCode£@codeListValue:"].values[0]
        except:
            Status = ""
        try:
            Freq_maj = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceMaintenance£gmd:MD_MaintenanceInformation£gmd:maintenanceAndUpdateFrequency£gmd:MD_MaintenanceFrequencyCode£@codeListValue:"].values[0]
        except:
            Freq_maj = ""

        Type_dates = []
        Dates = []
        try:
            for li in range(len(df)):
                if df.loc[li,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:dateType£gmd:CI_DateTypeCode£@codeListValue:":
                    Type_dates.append(df.loc[li,'Valeurs'])
        except:
            pass
        try:
            for l in range(len(df)):
                if df.loc[l,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:date£gco:Date£#text:":
                    Dates.append(df.loc[l,'Valeurs'])
        except:
            pass
        liste_dates = []
        try:
            for da in range(len(Type_dates)):
                liste_dates.append([Type_dates[da],Dates[da]])
        except:
            pass

        try:
            SupplementInfo = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:supplementalInformation£gco:CharacterString£#text:"].values[0]
        except:
            SupplementInfo = ""

        Liste_Theme = []
        Liste_Thesaurus = []
        Mots_cles = []
        Mots_cles_zaaj = []
        if 'zaaj_' in identifieur: 
            try:
                for u in range(len(df)):
                    if df.loc[u,'Clés']=="dc:subject£#text:":
                        Mots_cles_zaaj.append(df.loc[u,'Valeurs'])
            except:
                pass
        else:
            try:
                for u in range(len(df)):
                    if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:type£gmd:MD_KeywordTypeCode£@codeListValue:":
                        Liste_Theme.append([u,df.loc[u,'Valeurs']])
            except:
                pass
            try:
                for u in range(len(df)):
                    if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:thesaurusName£gmd:CI_Citation£gmd:title£gco:CharacterString£#text:":
                        Liste_Thesaurus.append([u,df.loc[u,'Valeurs']])
            except:
                pass
            try:
                for u in range(len(df)):
                    if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:keyword£gco:CharacterString£#text:" or  df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:keyword£gmx:Anchor£#text:":
                        Mots_cles.append([u,df.loc[u,'Valeurs']])
            except:
                pass

        theme_thesaurus_motsCles = []
        mm = 0    
        for th in range(1):
            liste_mots_cles = []
            try:
                if Liste_Theme[th][0]< Liste_Thesaurus[th][0]:
                    for m in range(mm,len(Mots_cles)):
                        if Mots_cles[m][0]<Liste_Theme[th][0]:
                            liste_mots_cles.append(Mots_cles[m][1])
                            mm = m
                    theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],Liste_Thesaurus[th][1]])
            except:
                try:
                    for m in range(mm,len(Mots_cles)):
                        if Mots_cles[m][0]<Liste_Theme[th][0]:
                            liste_mots_cles.append(Mots_cles[m][1])
                            mm = m
                    theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],"Aucun thésaurus"])
                except:
                    theme_thesaurus_motsCles.append([liste_mots_cles,"Aucun thème","Aucun thésaurus"])

        for th in range(1,len(Liste_Theme)):
            liste_mots_cles = []
            try:
                if Liste_Theme[th][0]< Liste_Thesaurus[th][0]:
                    for m in range(mm+1,len(Mots_cles)):
                        if Mots_cles[m][0]<Liste_Theme[th][0]:
                            liste_mots_cles.append(Mots_cles[m][1])
                            mm = m
                    theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],Liste_Thesaurus[th][1]])
            except:
                try:
                    for m in range(mm+1,len(Mots_cles)):
                        if Mots_cles[m][0]<Liste_Theme[th][0]:
                            liste_mots_cles.append(Mots_cles[m][1])
                            mm = m
                    theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],"Aucun thésaurus"])
                except:
                    theme_thesaurus_motsCles.append([liste_mots_cles,"Aucun thème","Aucun thésaurus"])

        Thesaurus = []
        for i in range(len(Liste_Thesaurus)):
            Thesaurus.append(Liste_Thesaurus[i][1])

        Themes = []
        for i in range(len(Liste_Theme)):
            Themes.append(Liste_Theme[i][1])

        if 'zaaj_' in identifieur: 
            Keywords = Mots_cles_zaaj
        else:
            Keywords = []
            for i in range(len(Mots_cles)):
                Keywords.append(Mots_cles[i][1])

        mention = 'Aucune mention'
        Titre_Keywords = Titre.split()
        for k in Keywords:
            Titre_Keywords.append(k)

        for s in Titre_Keywords:
            if s in filtre_mention:
                mention = s
            else:
                pass

        try:
            UseLimitation = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:useLimitation£gco:CharacterString£#text:"].values[0]
        except:
            UseLimitation =""

        if 'zaaj_' in identifieur:
            try:
                UseContrainte = df['Valeurs'][df['Clés']=="dc:rights£#text:"].values
            except:
                UseContrainte =""
        else:
            try:
                UseContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:useConstraints£gmd:MD_RestrictionCode£@codeListValue:"].values[0]
            except:
                UseContrainte =""
        try:
            AccesContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:accessConstraints£gmd:MD_RestrictionCode£@codeListValue:"].values[0]
        except:
            AccesContrainte =""
        try:
            AutreContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:otherConstraints£gco:CharacterString£#text:"].values[0]
        except:
            AutreContrainte =""

        if 'zaaj_' in identifieur:
            try:                        
                Format = df['Valeurs'][df['Clés']=="dc:format£#text:"].values
            except:
                Format = ""
        else:
            try:
                Format = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:distributionFormat£gmd:MD_Format£gmd:name£gco:CharacterString£#text:"].values
            except:
                Format = ""

        if 'zaaj_' in identifieur:
            try:
                Online_links = df['Valeurs'][df['Clés']=="dc:relation£#text:"].values
            except:
                Online_links = ""
        else:
            try:
                Online_links = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:linkage£gmd:URL:"].values
            except:
                Online_links = ""
        try:
            Online_protocols = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:protocol£gco:CharacterString£#text:"].values
        except:
            Online_protocols = ""
        try:
            Online_nom = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:name£gco:CharacterString£#text:"].values
        except:
            Online_nom = ""
        try:
            Online_description = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:description£gco:CharacterString£#text:"].values
        except:
            Online_description = ""

        try:
            Niveau = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:scope£gmd:DQ_Scope£gmd:level£gmd:MD_ScopeCode£@codeListValue:"].values[0]
        except:
            Niveau = ""
        try:
            Conformite = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:report£gmd:DQ_DomainConsistency£gmd:result£gmd:DQ_ConformanceResult£gmd:pass£gco:Boolean£#text:"].values[0]
        except:
            Conformite = ""
        try:
            Genealogie = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:lineage£gmd:LI_Lineage£gmd:statement£gco:CharacterString£#text:"].values[0]
        except:
            Genealogie = ""
        try:
            Scope = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:scope£gmd:DQ_Scope£gmd:levelDescription£gmd:MD_ScopeDescription£gmd:attributes£#text:"].values[0]
        except:
            Scope = ""

        """if 'oai:search-data.ubfc.fr' in identifieur:
            identifieur = identifieur.replace('zaaj_','oai:search-data.ubfc.fr:')
            try:
                groupe = df_infos['Groupe'][df_infos.Identifiant==identifieur].values[0]
            except:
                groupe = ""
            identifieur = identifieur.replace('oai:search-data.ubfc.fr:','zaaj_')
        else:
            try:
                groupe = df_infos['Groupe'][df_infos.Identifiant==identifieur].values[0]
            except:
                groupe = ""

        groupe_et_mention = ''
        try:
            if groupe == "Aucun groupe" and mention != "Aucune mention":
                groupe_et_mention = mention
            elif groupe != "Aucun groupe":
                groupe_et_mention = groupe
            elif groupe == "Aucun groupe" and mention == "Aucune mention":
                groupe_et_mention = "pas d'infos"
        except:
            pass"""

        liste_variables = [identifieur, Langue, JeuDeCaracteres, Type, Date, Standard, Version_standard, Nom_contact, Organisation_contact,
                        Position_contact, Tel_contact, DeliveryPoint, CodePostal, Ville, Pays, Email, SystemReference,
                        westBoundLongitude, EastBoundLongitude, SouthBoundLatitude, NorthBoundLatitude, Titre,
                        FicheParent, Abstract, Date_creation, Purpose, Status, Freq_maj, liste_dates, SupplementInfo,
                        UseLimitation, UseContrainte, AccesContrainte, AutreContrainte,
                        Format, Online_links, Online_protocols, Online_description, Online_nom,
                        Niveau, Conformite, Genealogie, Scope, mention, Thesaurus, Themes, Keywords, theme_thesaurus_motsCles]

        liste_columns_df = ['Identifiant', 'Langue', 'Jeu de caractères', 'Type', 'Date', 'Nom du standard', 'Version du standard', 'Nom du contact', 'orga du contact',
                            'Position du contact', 'Tel du contact', 'Adresse', 'Code Postal', 'Ville', 'Pays', 'Email du contact', "Systeme de référence",
                            'Longitude ouest', 'Longitude est', 'Latitude sud', 'Latitude nord', 'Titre',
                            'Fiche parent id', 'Résumé', "Date de création", 'Objectif', 'Status', 'Fréquence de maj', 'Autres dates', 'Info supplémentaire',
                            'Limite usage', 'Contrainte usage', 'Contrainte accès', 'Autre contrainte',
                            'Format', 'Url', 'Protocole', 'Online description', 'Online nom',
                            'Niveau', 'Conformité', 'Généalogie', 'Portée','Mention du groupe', 'Thesaurus', 'Thèmes', 'Mots Clés', 'theme_thesaurus_motsCles']
            
        df_variables_evaluation = pd.DataFrame(data=[liste_variables],columns=liste_columns_df)  

    return df_variables_evaluation


#################################################################################
###################################################################################
##############################################################################""""


def recup_fiche(url, identifieur, headers_json, headers_xml, couleur_True, couleur_False, df_infos, filtre_mention):
    try:
        if 'oai:search-data.ubfc.fr:' in identifieur:
            identifieur = identifieur.replace('oai:search-data.ubfc.fr:','zaaj_')
            df = pd.read_csv(f'pages/data/fiches_csv/{identifieur}.csv',index_col=[0])
            F1 = True
            F1c = couleur_True
            A2 = True
            A2c = couleur_True
        else:
            df = pd.read_csv(f'pages/data/fiches_csv/{identifieur}.csv',index_col=[0])
            F1 = True
            F1c = couleur_True
            A2 = True
            A2c = couleur_True
    except:
        if 'zaaj_' in identifieur:
            identifieur = identifieur.replace('zaaj_','oai:search-data.ubfc.fr:')
        url_ = url + identifieur
        resp1 = requests.get(url_,headers=headers_json)
        if resp1.status_code == 200:
            resp_json=resp1.json()
            try:
                if 'oai:search-data.ubfc.fr:' in identifieur:
                    identifieur = identifieur.replace('oai:search-data.ubfc.fr:','zaaj_')
                    with open(f"pages/data/fiches_json/{identifieur}.json", "w") as f:
                        json.dump(resp_json, f, indent=4)
                else:
                    with open(f"pages/data/fiches_json/{identifieur}.json", "w") as f:
                        json.dump(resp_json, f, indent=4)
            except:
                pass
        
        resp2 = requests.get(url_,headers=headers_xml)
        if resp2.status_code == 200:
            xml_content = resp2.text
            try:
                with open(f"pages/data/fiches_xml/{identifieur}.xml", 'w') as file:
                    file.write(xml_content)
            except:
                pass

        url_asso = url_ +"/associated?rows=100"
        resp_asso = requests.get(url_asso,headers=headers_json)
        if resp_asso.status_code == 200:
            resp_asso_json=resp_asso.json()
            try:
                with open(f"pages/data/associated_resources/resource_{identifieur}.json", "w") as f:
                    json.dump(resp_asso_json, f, indent=4)
            except:
                pass

        url_attach = url_ +"/attachments"
        resp_attach = requests.get(url_attach,headers=headers_json)
        if resp_attach.status_code == 200:
            resp_attach_json=resp_attach.json()
            try:
                with open(f"pages/data/attachments/attachments_{identifieur}.json", "w") as f:
                    json.dump(resp_attach_json, f, indent=4)
            except:
                pass

    try:
        if 'oai:search-data.ubfc.fr:' in identifieur:
            identifieur = identifieur.replace('oai:search-data.ubfc.fr:','zaaj_')
        with open(f"pages/data/fiches_json/{identifieur}.json", 'r') as f:
            data = json.load(f)

        with open(f'pages/data/fiches_txt/{identifieur}.txt', 'w') as file:
            transcript_json(data, file)

        with open(f'pages/data/fiches_txt/{identifieur}.txt', 'r') as f:
            d = f.read()

        listi = re.split('µ',d)

        df = pd.DataFrame(listi, columns=['Results'])
        for u in range(len(df)):
            p = re.split('§',df.loc[u,'Results'])
            try:
                df.loc[u,'Valeurs']=p[1]
            except:
                pass
            try:
                df.loc[u,'Clés']=p[0].replace('.','£')
            except:
                pass

        for j in range(len(df)):
            pp = re.split('£',df.loc[j,'Clés'])
            for k in range(15):
                try:
                    df.loc[j,f'K{k}']=pp[k]
                except:
                    pass
        df.to_csv(f'pages/data/fiches_csv/{identifieur}.csv')
        F1 = True
        F1c = couleur_True
        A2 = True
        A2c = couleur_True
    except:
        F1 = False
        F1c = couleur_False
        A2 = False
        A2c = couleur_False

    if "zaaj_" in identifieur:
        try:
            Langue = df['Valeurs'][df['Clés']=="dc:title£@xml:lang:"].values
        except:
            Langue = ""
    else:
        try:
            Langue = df['Valeurs'][df['Clés']=="gmd:language£gco:CharacterString£#text:"].values[0]
        except:
            try:
                Langue = df['Valeurs'][df['Clés']=="gmd:language£gmd:LanguageCode£@codeListValue:"].values[0]
            except:
                Langue = ""
    try:
        JeuDeCaracteres = df['Valeurs'][df['Clés']=="gmd:characterSet£gmd:MD_CharacterSetCode£@codeListValue:"].values[0]
    except:
        JeuDeCaracteres =""
    try:
        Type = df['Valeurs'][df['Clés']=="gmd:hierarchyLevel£gmd:MD_ScopeCode£@codeListValue:"].values[0]
    except:
        try:
            Type = df['Valeurs'][df['Clés']=="gfc:featureType£gfc:FC_FeatureType£gfc:typeName£gco:LocalName£#text:"].values[0]
        except:
            try:
                Type = df['Valeurs'][df['Clés']=="dc:type£#text:"].values[0]
            except:
                Type =""
    try:
        Date = df['Valeurs'][df['Clés']=="gmd:dateStamp£gco:DateTime£#text:"].values[0]
    except:
        try:
            Date = df['Valeurs'][df['Clés']=="gfc:versionDate£gco:DateTime£#text:"].values[0]
        except:
            try:
                Date = df['Valeurs'][df['Clés']=="gmx:versionDate£gco:DateTime£#text:"].values[0]
            except:
                try:
                    Date = df['Valeurs'][df['Clés']=="dc:date£#text:"].values[0]
                except:
                    Date = ""

    if 'zaaj_' in identifieur:  
        try:                      
            Standard = df['Valeurs'][df['Clés']=="@xsi:noNamespaceSchemaLocation:"].values[0]
        except:
            Standard = ""
    else:
        try:
            Standard = df['Valeurs'][df['Clés']=="gmd:metadataStandardName£gco:CharacterString£#text:"].values[0]
        except:
            try:
                Standard = df['Valeurs'][df['Clés']=="gfc:name£gco:CharacterString£@xmlns:gco:"].values[0]
            except:
                Standard = ""
    try:
        Version_standard = df['Valeurs'][df['Clés']=="gmd:metadataStandardVersion£gco:CharacterString£#text:"].values[0]
    except:
        Version_standard = ""

    if 'zaaj_' in identifieur:    
        try:                    
            Nom_contact = df['Valeurs'][df['Clés']=="dc:creator£#text:"].values
        except:
            Nom_contact = ""
    else:
        try:
            Nom_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values
            if len(Nom_contact)==0:
                Nom_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values
        except:
            try:
                Nom_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values
            except:
                try:
                    Nom_contact = df['Valeurs'][df['Clés']=="gfc:producer£gmd:CI_ResponsibleParty£gmd:individualName£gco:CharacterString£#text:"].values[0]
                except: 
                    Nom_contact = ""

    if 'zaaj_' in identifieur:  
        try:                      
            Organisation_contact = df['Valeurs'][df['Clés']=="dc:publisher£#text:"].values
        except:
            Organisation_contact = ""
    else:
        try:
            Organisation_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values
            if len(Organisation_contact)==0:
                Organisation_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values
        except:
            try:
                Organisation_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:organisationName£gco:CharacterString£#text:"].values
            except:
                Organisation_contact = ""
    try:
        Position_contact =df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values
        if len(Position_contact)==0:
            Position_contact =df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values
    except:
        try:
            Position_contact =df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:positionName£gco:CharacterString£#text:"].values
        except:
            Position_contact = ""
    try:
        Tel_contact = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values
        if len(Tel_contact)==0:
            Tel_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values
    except:
        try:
            Tel_contact = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:phone£gmd:CI_Telephone£gmd:voice£gco:CharacterString£#text:"].values
        except:
            Tel_contact = ""
    try:
        DeliveryPoint = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:deliveryPoint£gco:CharacterString£#text:"].values
        if len(DeliveryPoint)==0:
            DeliveryPoint = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:deliveryPoint£gco:CharacterString£#text:"].values
    except:
        try:
            DeliveryPoint = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:deliveryPoint£gco:CharacterString£#text:"].values
        except:
            DeliveryPoint = ""
    try:
        CodePostal = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:postalCode£gco:CharacterString£#text:"].values
        if len(CodePostal)==0:
            CodePostal = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:postalCode£gco:CharacterString£#text:"].values
    except:
        try:
            CodePostal = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:postalCode£gco:CharacterString£#text:"].values
        except:
            CodePostal = ""
    try:
        Ville = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:city£gco:CharacterString£#text:"].values
        if len(Ville)==0:
            Ville = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:city£gco:CharacterString£#text:"].values
    except:
        try:
            Ville = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:city£gco:CharacterString£#text:"].values
        except:
            Ville = ""
    try:
        Pays = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:country£gco:CharacterString£#text:"].values
        if len(Pays)==0:
            Pays = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:country£gco:CharacterString£#text:"].values
    except:
        try:
            Pays = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:country£gco:CharacterString£#text:"].values
        except:
            Pays =""
    try:
        Email = df['Valeurs'][df['Clés']=="gmd:contact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:electronicMailAddress£gco:CharacterString£#text:"].values[0]
    except:
        try:
            Email = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:pointOfContact£gmd:CI_ResponsibleParty£gmd:contactInfo£gmd:CI_Contact£gmd:address£gmd:CI_Address£gmd:electronicMailAddress£gco:CharacterString£#text:"].values[0]
        except:
            Email = ""


    try:
        SystemReference =  df['Valeurs'][df['Clés']=="gmd:referenceSystemInfo£gmd:MD_ReferenceSystem£gmd:referenceSystemIdentifier£gmd:RS_Identifier£gmd:code£gco:CharacterString£#text:"].values
    except:
        SystemReference = ""
    try:
        westBoundLongitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:westBoundLongitude£gco:Decimal£#text:"].values[0]
    except:
        westBoundLongitude = ""
    try:
        EastBoundLongitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:eastBoundLongitude£gco:Decimal£#text:"].values[0]
    except:
        EastBoundLongitude = ""
    try:
        SouthBoundLatitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:southBoundLatitude£gco:Decimal£#text:"].values[0]
    except:
        SouthBoundLatitude = ""
    try:
        NorthBoundLatitude = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:extent£gmd:EX_Extent£gmd:geographicElement£gmd:EX_GeographicBoundingBox£gmd:northBoundLatitude£gco:Decimal£#text:"].values[0]
    except:
        NorthBoundLatitude = ""

    try: 
        Titre = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:title£gco:CharacterString£#text:"].values[0]
    except:
        try:
            Titre = df['Valeurs'][df['Clés']=="gfc:name£gco:CharacterString£#text:"].values[0]
        except:
            try:
                Titre = df['Valeurs'][df['Clés']=="dc:title£#text:"].values[0]
            except:
                Titre = ""
    try: 
        FicheParent = df['Valeurs'][df['Clés']=="gmd:parentIdentifier£gco:CharacterString£#text:"].values[0]
    except:
        FicheParent = ""

    if 'zaaj_' in identifieur:
        try:
            Abstract =df['Valeurs'][df['Clés']=="dc:description£#text:"].values
        except:
            Abstract = ""
    else:
        try:
            Abstract =df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:abstract£gco:CharacterString£#text:"].values[0]
        except:
            Abstract = ""

    try:
        Date_creation = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:date£gco:DateTime£#text:"].values[0]
    except:
        Date_creation = ""
    try:
        Purpose = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:purpose£gco:CharacterString£#text:"].values[0]
    except:
        Purpose = ""
    try:
        Status = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:status£gmd:MD_ProgressCode£@codeListValue:"].values[0]
    except:
        Status = ""
    try:
        Freq_maj = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceMaintenance£gmd:MD_MaintenanceInformation£gmd:maintenanceAndUpdateFrequency£gmd:MD_MaintenanceFrequencyCode£@codeListValue:"].values[0]
    except:
        Freq_maj = ""

    Type_dates = []
    Dates = []
    try:
        for li in range(len(df)):
            if df.loc[li,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:dateType£gmd:CI_DateTypeCode£@codeListValue:":
                Type_dates.append(df.loc[li,'Valeurs'])
    except:
        pass
    try:
        for l in range(len(df)):
            if df.loc[l,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:citation£gmd:CI_Citation£gmd:date£gmd:CI_Date£gmd:date£gco:Date£#text:":
                Dates.append(df.loc[l,'Valeurs'])
    except:
        pass
    liste_dates = []
    try:
        for da in range(len(Type_dates)):
            liste_dates.append([Type_dates[da],Dates[da]])
    except:
        pass

    try:
        SupplementInfo = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:supplementalInformation£gco:CharacterString£#text:"].values[0]
    except:
        SupplementInfo = ""

    Liste_Theme = []
    Liste_Thesaurus = []
    Mots_cles = []
    Mots_cles_zaaj = []
    if 'zaaj_' in identifieur: 
        try:
            for u in range(len(df)):
                if df.loc[u,'Clés']=="dc:subject£#text:":
                    Mots_cles_zaaj.append(df.loc[u,'Valeurs'])
        except:
            pass
    else:
        try:
            for u in range(len(df)):
                if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:type£gmd:MD_KeywordTypeCode£@codeListValue:":
                    Liste_Theme.append([u,df.loc[u,'Valeurs']])
        except:
            pass
        try:
            for u in range(len(df)):
                if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:thesaurusName£gmd:CI_Citation£gmd:title£gco:CharacterString£#text:":
                    Liste_Thesaurus.append([u,df.loc[u,'Valeurs']])
        except:
            pass
        try:
            for u in range(len(df)):
                if df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:keyword£gco:CharacterString£#text:" or  df.loc[u,'Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:descriptiveKeywords£gmd:MD_Keywords£gmd:keyword£gmx:Anchor£#text:":
                    Mots_cles.append([u,df.loc[u,'Valeurs']])
        except:
            pass

    theme_thesaurus_motsCles = []
    mm = 0    
    for th in range(1):
        liste_mots_cles = []
        try:
            if Liste_Theme[th][0]< Liste_Thesaurus[th][0]:
                for m in range(mm,len(Mots_cles)):
                    if Mots_cles[m][0]<Liste_Theme[th][0]:
                        liste_mots_cles.append(Mots_cles[m][1])
                        mm = m
                theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],Liste_Thesaurus[th][1]])
        except:
            try:
                for m in range(mm,len(Mots_cles)):
                    if Mots_cles[m][0]<Liste_Theme[th][0]:
                        liste_mots_cles.append(Mots_cles[m][1])
                        mm = m
                theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],"Aucun thésaurus"])
            except:
                theme_thesaurus_motsCles.append([liste_mots_cles,"Aucun thème","Aucun thésaurus"])

    for th in range(1,len(Liste_Theme)):
        liste_mots_cles = []
        try:
            if Liste_Theme[th][0]< Liste_Thesaurus[th][0]:
                for m in range(mm+1,len(Mots_cles)):
                    if Mots_cles[m][0]<Liste_Theme[th][0]:
                        liste_mots_cles.append(Mots_cles[m][1])
                        mm = m
                theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],Liste_Thesaurus[th][1]])
        except:
            try:
                for m in range(mm+1,len(Mots_cles)):
                    if Mots_cles[m][0]<Liste_Theme[th][0]:
                        liste_mots_cles.append(Mots_cles[m][1])
                        mm = m
                theme_thesaurus_motsCles.append([liste_mots_cles,Liste_Theme[th][1],"Aucun thésaurus"])
            except:
                theme_thesaurus_motsCles.append([liste_mots_cles,"Aucun thème","Aucun thésaurus"])

    Thesaurus = []
    for i in range(len(Liste_Thesaurus)):
        Thesaurus.append(Liste_Thesaurus[i][1])

    Themes = []
    for i in range(len(Liste_Theme)):
        Themes.append(Liste_Theme[i][1])

    if 'zaaj_' in identifieur: 
        Keywords = Mots_cles_zaaj
    else:
        Keywords = []
        for i in range(len(Mots_cles)):
            Keywords.append(Mots_cles[i][1])

    mention = 'Aucune mention'
    Titre_Keywords = Titre.split()
    for k in Keywords:
        Titre_Keywords.append(k)

    for s in Titre_Keywords:
        if s in filtre_mention:
            mention = s
        else:
            pass

    try:
        UseLimitation = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:useLimitation£gco:CharacterString£#text:"].values[0]
    except:
        UseLimitation =""

    if 'zaaj_' in identifieur:
        try:
            UseContrainte = df['Valeurs'][df['Clés']=="dc:rights£#text:"].values
        except:
            UseContrainte =""
    else:
        try:
            UseContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:useConstraints£gmd:MD_RestrictionCode£@codeListValue:"].values[0]
        except:
            UseContrainte =""
    try:
        AccesContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:accessConstraints£gmd:MD_RestrictionCode£@codeListValue:"].values[0]
    except:
        AccesContrainte =""
    try:
        AutreContrainte = df['Valeurs'][df['Clés']=="gmd:identificationInfo£gmd:MD_DataIdentification£gmd:resourceConstraints£gmd:MD_LegalConstraints£gmd:otherConstraints£gco:CharacterString£#text:"].values[0]
    except:
        AutreContrainte =""

    if 'zaaj_' in identifieur:
        try:                        
            Format = df['Valeurs'][df['Clés']=="dc:format£#text:"].values
        except:
            Format = ""
    else:
        try:
            Format = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:distributionFormat£gmd:MD_Format£gmd:name£gco:CharacterString£#text:"].values
        except:
            Format = ""

    if 'zaaj_' in identifieur:
        try:
            Online_links = df['Valeurs'][df['Clés']=="dc:relation£#text:"].values
        except:
            Online_links = ""
    else:
        try:
            Online_links = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:linkage£gmd:URL:"].values
        except:
            Online_links = ""
    try:
        Online_protocols = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:protocol£gco:CharacterString£#text:"].values
    except:
        Online_protocols = ""
    try:
        Online_nom = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:name£gco:CharacterString£#text:"].values
    except:
        Online_nom = ""
    try:
        Online_description = df['Valeurs'][df['Clés']=="gmd:distributionInfo£gmd:MD_Distribution£gmd:transferOptions£gmd:MD_DigitalTransferOptions£gmd:onLine£gmd:CI_OnlineResource£gmd:description£gco:CharacterString£#text:"].values
    except:
        Online_description = ""

    try:
        Niveau = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:scope£gmd:DQ_Scope£gmd:level£gmd:MD_ScopeCode£@codeListValue:"].values[0]
    except:
        Niveau = ""
    try:
        Conformite = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:report£gmd:DQ_DomainConsistency£gmd:result£gmd:DQ_ConformanceResult£gmd:pass£gco:Boolean£#text:"].values[0]
    except:
        Conformite = ""
    try:
        Genealogie = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:lineage£gmd:LI_Lineage£gmd:statement£gco:CharacterString£#text:"].values[0]
    except:
        Genealogie = ""
    try:
        Scope = df['Valeurs'][df['Clés']=="gmd:dataQualityInfo£gmd:DQ_DataQuality£gmd:scope£gmd:DQ_Scope£gmd:levelDescription£gmd:MD_ScopeDescription£gmd:attributes£#text:"].values[0]
    except:
        Scope = ""

    if 'zaaj_' in identifieur:
        identifieur = identifieur.replace('zaaj_','oai:search-data.ubfc.fr:')
        try:
            groupe = df_infos['Groupe'][df_infos.Identifiant==identifieur].values[0]
        except:
            groupe = ""
        identifieur = identifieur.replace('oai:search-data.ubfc.fr:','zaaj_')
    else:
        try:
            groupe = df_infos['Groupe'][df_infos.Identifiant==identifieur].values[0]
        except:
            groupe = ""

    groupe_et_mention = ''
    try:
        if groupe == "Aucun groupe" and mention != "Aucune mention":
            groupe_et_mention = mention
        elif groupe != "Aucun groupe":
            groupe_et_mention = groupe
        elif groupe == "Aucun groupe" and mention == "Aucune mention":
            groupe_et_mention = "pas d'infos"
    except:
        pass

    if len(Titre)!=0 and len(Abstract)!=0 and len(Organisation_contact)!=0 and len(Nom_contact)!=0 and len(Email)!=0:
        F2 = True
        F2c = couleur_True
    else:
        F2 = False
        F2c = couleur_False

    if len(Online_links)!=0:
        for i in range(len(Online_links)):
            if 'doi' in Online_links[i] or 'attachments' in Online_links[i]:
                A1 = True
                A1c = couleur_True
                F3 = True
                F3c = couleur_True
            else:
                A1 = False
                A1c = couleur_False
                F3 = False
                F3c = couleur_False
    else:
        A1 = False
        A1c = couleur_False
        F3 = False
        F3c = couleur_False

    if groupe in (['Aucun groupe', 'Groupe exemple']):
        F4 = False
        F4c = couleur_False
    else:
        F4 = True
        F4c = couleur_True

    if len(Format)!=0:
        for i in range(len(Format)):
            if Format[i] in ['GeoTiff','GeoTIFF', 'GEOTIFF','shape','ESRI Shapefile','Word','ASC','CSV','png','PNG','pdf','PDF','svg','SVG', 'odt','ODT','rtf', 'RTF','txt','TXT','jpg','JPG','ods','ODS','mkv','MKV','zip','ZIP','tar','TAR']:
                I1 = True
                I1c = couleur_True
            else:
                I1 = False
                I1c = couleur_False
    else:
        I1 = False
        I1c = couleur_False

    if len(Thesaurus)==0:
        I2 = False
        I2c = couleur_False
    else:
        I2 = True
        I2c = couleur_True

    if len(Keywords)==0:
        I3 = False
        I3c = couleur_False
    else:
        I3 = True
        I3c = couleur_True

    if len(UseLimitation)==0 and  len(UseContrainte)==0 and len(AccesContrainte)==0 and len(AutreContrainte)==0:
        R1 = False
        R1c = couleur_False
    elif len(UseContrainte)!=0 or len(UseLimitation)!=0:
        R1 = True
        R1c = couleur_True
    else:
        R1 = False
        R1c = couleur_False

    if len(Genealogie)==0:
        R2 = False
        R2c = couleur_False
    else:
        R2 = True
        R2c = couleur_True

    R3 = False
    R3c = couleur_False

    liste_variables = [identifieur, Langue, JeuDeCaracteres, Type, Date, Standard, Version_standard, Nom_contact, Organisation_contact,
                   Position_contact, Tel_contact, DeliveryPoint, CodePostal, Ville, Pays, Email, SystemReference,
                   westBoundLongitude, EastBoundLongitude, SouthBoundLatitude, NorthBoundLatitude, Titre,
                   FicheParent, Abstract, Date_creation, Purpose, Status, Freq_maj, liste_dates, SupplementInfo,
                   UseLimitation, UseContrainte, AccesContrainte, AutreContrainte,
                   Format, Online_links, Online_protocols, Online_description, Online_nom,
                   Niveau, Conformite, Genealogie, Scope, groupe, mention, Thesaurus, Themes, Keywords, 
                   F1, F2, F3, F4, A1, A2, I1, I2, I3, R1, R2, R3]

    liste_variables2 = [identifieur, Langue, Date, Standard, Version_standard, Nom_contact, Organisation_contact,
                        Position_contact,westBoundLongitude, EastBoundLongitude, SouthBoundLatitude, NorthBoundLatitude,Titre,
                        Thesaurus,Themes, Keywords, UseLimitation, UseContrainte, Format,Online_links, F2, A1,I1,I2,R1,R2,groupe_et_mention]  

    liste_columns_df = ['Identifiant', 'Langue', 'Jeu de caractères', 'Type', 'Date', 'Nom du standard', 'Version du standard', 'Nom du contact', 'orga du contact',
                    'Position du contact', 'Tel du contact', 'Adresse', 'Code Postal', 'Ville', 'Pays', 'Email du contact', "Systeme de référence",
                    'Longitude ouest', 'Longitude est', 'Latitude sud', 'Latitude nord', 'Titre',
                    'Fiche parent id', 'Résumé', "Date de création", 'Objectif', 'Status', 'Fréquence de maj', 'Autres dates', 'Info supplémentaire',
                    'Limite usage', 'Contrainte usage', 'Contrainte accès', 'Autre contrainte',
                    'Format', 'Url', 'Protocole', 'Online description', 'Online nom',
                    'Niveau', 'Conformité', 'Généalogie', 'Portée', 'Groupe associé','Mention du groupe', 'Thesaurus', 'Thèmes', 'Mots Clés',
                    'F1', 'F2', 'F3', 'F4', 'A1', 'A2', 'I1', 'I2', 'I3', 'R1', 'R2', 'R3']
    
    liste_columns_df2 = ['Identifiant','Langue','Date','Standard','Version_standard','Nom_contact','Orga_contact',
                         'Position_contact','Longitude_Ouest','Longitude_Est','Latitude_Sud','Latitude_Nord','Titre',
                         'Thesaurus','Themes','Mots_clés','Limite_usage','Contrainte_usage','Format','URL','F2','A1','I1','I2','R1','R2','Groupe_et_Mention']


    df_variables_evaluation = pd.DataFrame(data=[liste_variables2],columns=liste_columns_df2)

    return df_variables_evaluation, mention, groupe_et_mention