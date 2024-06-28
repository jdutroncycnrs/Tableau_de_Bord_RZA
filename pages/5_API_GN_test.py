import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
pd.options.mode.chained_assignment = None

fichier= "uuid_GNdeTest"
######################## URL de l'API ##############################
url = "http://localhost:8080/geonetwork/srv/api/records/"
####################################################################

headers = {"accept":"application/json",
           "X-XSRF-TOKEN": "e12ff8ca-7362-413d-9e27-a2aa1426f0b4"}

### Récupération des variables choisies dans les fiches du GN ######


if __name__=="__main__":
    """data = pd.read_csv(f"pages/data/{fichier}.csv")
    cles_json=[]
    for l in range(len(data)):
        i = data.values[l][0]

        url_ = url + i

        resp = requests.get(url_,headers=headers)
        st=resp.json()
        cles = list(st.keys())
        data.loc[l,"nb_champs_renseignés"]=len(cles)
        cles_json.append(cles)
    
    data.to_csv(f"pages/data/{fichier}_.csv")

    data2 = pd.DataFrame(cles_json)
    data2.to_csv("pages/data/cles_json.csv")"""

    """data = pd.read_csv(f"pages/data/{fichier}_.csv")
    m = max(data['nb_champs_renseignés'])
    i = data['uuid'][data["nb_champs_renseignés"]==m]
    url_ = url + data.loc[89, "uuid"]
    resp = requests.get(url_,headers=headers)
    st=resp.json()
    cles = list(st.keys())
    print(cles)"""

    """cles = pd.read_csv("pages/data/cles_json.csv")
    cles.drop(columns=['Unnamed: 0'], inplace=True)
    l = []
    for i in range(len(cles)):
        li = list(cles.loc[i,:].values)
        for j in range(len(li)):
            l.append(li[j])

    cles_tot = pd.DataFrame(l,columns=['cles'])
    cles_tot.to_csv("pages/data/cles_tot.csv")"""

    cles_t = pd.read_csv("pages/data/cles_tot.csv")
    cles_t.drop(columns=['Unnamed: 0'], inplace=True)
    cles_t.dropna(axis=0,inplace=True)
    cl = list(cles_t["cles"].unique())
    

    u = '87222542-80d3-4326-9957-2108c8e225e6'
    url_ = url + u
    resp = requests.get(url_,headers=headers)
    st=resp.json()

    with open("pages/data/json_test.json", "w") as f:
        json.dump(st, f, indent=4)
    
    for c in cl:
        try:
            if c=="gmd:fileIdentifier":
                print("fileIdentifier/len=",len(st[c]))
                print("identifier=",st[c]['gco:CharacterString']['#text'])
                print("\n")
            elif c=="gmd:hierarchyLevel":
                print("hierarchyLevel/len=",len(st[c]))
                print("gml=",st[c]['@xmlns:gml'])
                print("gn=",st[c]['@xmlns:gn'])
                print("hierarchyLevel/MD_ScopeCode/len=",len(st[c]['gmd:MD_ScopeCode']))
                print("hierarchyLevel/MD_ScopeCode/codeList=",st[c]['gmd:MD_ScopeCode']['@codeList'])
                print("hierarchyLevel/MD_ScopeCode/codeListValue=",st[c]['gmd:MD_ScopeCode']['@codeListValue'])
                print("\n")
            elif c=="gmd:contact":
                print("contact/len=",len(st[c]))
                print("gml=",st[c]['@xmlns:gml'])
                print("contact/ResponsibleParty/len=",len(st[c]['gmd:CI_ResponsibleParty']))
                print("contact/ResponsibleParty/individualName/len=",len(st[c]['gmd:CI_ResponsibleParty']['gmd:individualName']))
                print("contact_responsable=",st[c]['gmd:CI_ResponsibleParty']['gmd:individualName']['gco:CharacterString']['#text'])
                print("contact/ResponsibleParty/organisationName/len=",len(st[c]['gmd:CI_ResponsibleParty']['gmd:organisationName']))
                print("organisation_name=",st[c]['gmd:CI_ResponsibleParty']['gmd:organisationName']['gco:CharacterString']['#text'])
                print("contact/ResponsibleParty/positionName/len=",len(st[c]['gmd:CI_ResponsibleParty']['gmd:positionName']))
                print(st[c]['gmd:CI_ResponsibleParty']['gmd:positionName'])
                print("position_name=",st[c]['gmd:CI_ResponsibleParty']['gmd:positionName']['gco:CharacterString'])
                print("contact_info_phone=",st[c]['gmd:CI_ResponsibleParty']["gmd:contactInfo"]["gmd:CI_Contact"]["gmd:phone"]["gmd:CI_Telephone"]["gmd:voice"]['gco:CharacterString'])
                print("contact_info_adresse=",st[c]['gmd:CI_ResponsibleParty']["gmd:contactInfo"]["gmd:CI_Contact"]["gmd:address"]["gmd:CI_Address"]["gmd:deliveryPoint"]['gco:CharacterString'])
                print("contact_info_city=",st[c]['gmd:CI_ResponsibleParty']["gmd:contactInfo"]["gmd:CI_Contact"]["gmd:address"]["gmd:CI_Address"]["gmd:city"]['gco:CharacterString'])
                print("contact_info_adminArea=",st[c]['gmd:CI_ResponsibleParty']["gmd:contactInfo"]["gmd:CI_Contact"]["gmd:address"]["gmd:CI_Address"]["gmd:administrativeArea"]['gco:CharacterString'])
                print("contact_info_postalCode=",st[c]['gmd:CI_ResponsibleParty']["gmd:contactInfo"]["gmd:CI_Contact"]["gmd:address"]["gmd:CI_Address"]["gmd:postalCode"]['gco:CharacterString'])
                print("contact_info_country=",st[c]['gmd:CI_ResponsibleParty']["gmd:contactInfo"]["gmd:CI_Contact"]["gmd:address"]["gmd:CI_Address"]["gmd:country"]['gco:CharacterString'])
                print("contact_info_email=",st[c]['gmd:CI_ResponsibleParty']["gmd:contactInfo"]["gmd:CI_Contact"]["gmd:address"]["gmd:CI_Address"]["gmd:electronicMailAddress"]['gco:CharacterString']['#text'])
            elif c=="gmd:dateStamp":
                print("date_record=",st[c]['gco:DateTime']['#text'])
            elif c=="gmd:metadataStandardName":
                print("MD_standard=",st[c]['gco:CharacterString']['#text'])
            elif c=="gmd:metadataStandardVersion":
                print("MD_standard_version=",st[c]['gco:CharacterString']['#text'])
            elif c=="gmd:referenceSystemInfo":
                print("Systeme_reference=",st[c]['gmd:MD_ReferenceSystem']['gmd:referenceSystemIdentifier']['gmd:RS_Identifier']['gmd:code']['gco:CharacterString']['#text'])
                print("Systeme_codespace=",st[c]['gmd:MD_ReferenceSystem']['gmd:referenceSystemIdentifier']['gmd:RS_Identifier']['gmd:codeSpace']['gco:CharacterString']['#text'])
                print("Systeme_version=",st[c]['gmd:MD_ReferenceSystem']['gmd:referenceSystemIdentifier']['gmd:RS_Identifier']['gmd:version']['gco:CharacterString']['#text'])
            elif c=="gmd:identificationInfo":
                #print(json.dumps(st[c],indent=4))
                print("titre=",st[c]["gmd:MD_DataIdentification"]["gmd:citation"]["gmd:CI_Citation"]["gmd:title"]['gco:CharacterString']['#text'])
                print("attention il y a plusieurs dates, par catégorie")
                print("date=",st[c]["gmd:MD_DataIdentification"]["gmd:citation"]["gmd:CI_Citation"]["gmd:date"])
                print("identif=",st[c]["gmd:MD_DataIdentification"]["gmd:citation"]["gmd:CI_Citation"]["gmd:identifier"]["gmd:MD_Identifier"]["gmd:code"]['gco:CharacterString']['#text'])
                print("presentation_form=",st[c]["gmd:MD_DataIdentification"]["gmd:citation"]["gmd:CI_Citation"]["gmd:presentationForm"]["gmd:CI_PresentationFormCode"]["@codeListValue"])
                print("identif=",st[c]["gmd:MD_DataIdentification"]["gmd:citation"]["gmd:CI_Citation"]["gmd:identifier"]["gmd:MD_Identifier"]["gmd:code"]['gco:CharacterString']['#text'])
                print("resume=",st[c]["gmd:MD_DataIdentification"]["gmd:abstract"]['gco:CharacterString']['#text'])
                print("status=",st[c]["gmd:MD_DataIdentification"]["gmd:status"]["gmd:MD_ProgressCode"]["@codeListValue"])
                print("attention il y a plusieurs contacts, par role")
                print("pointDeContact_individu=",st[c]["gmd:MD_DataIdentification"]["gmd:pointOfContact"]["gmd:CI_ResponsibleParty"]["gmd:individualName"]['gco:CharacterString']['#text'])
                print("pointDeContact_orga=",st[c]["gmd:MD_DataIdentification"]["gmd:pointOfContact"]["gmd:CI_ResponsibleParty"]["gmd:organisationName"]['gco:CharacterString']['#text'])
                print("pointDeContact_adresse=",st[c]["gmd:MD_DataIdentification"]["gmd:pointOfContact"]["gmd:CI_ResponsibleParty"]["gmd:contactInfo"]["gmd:CI_Contact"]["gmd:address"]["gmd:CI_Address"]["gmd:electronicMailAddress"]['gco:CharacterString']['#text'])
                print("pointDeContact_role=",st[c]["gmd:MD_DataIdentification"]["gmd:pointOfContact"]["gmd:CI_ResponsibleParty"]["gmd:role"]["gmd:CI_Contact"]["gmd:CI_RoleCode"]["@codeListValue"])
                print("maintenance=",st[c]["gmd:MD_DataIdentification"]["gmd:resourceMaintenance"]["gmd:MD_MaintenanceInformation"]["gmd:maintenanceAndUpdateFrequency"]["gmd:MD_MaintenanceFrequencyCode"]["@codeListValue"])
                print("Attention il y a plusieurs mots cles, par type")
                print("mots_cles=",st[c]["gmd:MD_DataIdentification"]["gmd:descriptiveKeywords"]["gmd:MD_Keywords"]["gmd:keyword"]['gco:CharacterString']['#text'])
                print("contraintes_usage=",st[c]["gmd:MD_DataIdentification"]["gmd:resourceConstraints"]["gmd:MD_LegalConstraints"]["gmd:useLimitation"]['gco:CharacterString']['#text'])
                print("contraintes_acces=",st[c]["gmd:MD_DataIdentification"]["gmd:resourceConstraints"]["gmd:MD_LegalConstraints"]["gmd:accessConstraints"]["gmd:MD_RestrictionCode"]["@codeListValue"])
        except: 
            pass
