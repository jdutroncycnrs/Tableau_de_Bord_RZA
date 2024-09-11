import requests
import json.decoder
from bs4 import BeautifulSoup as soup


def afficher_texte_reponse_api_hal(requete_api_hal: str):
    """Interroge l'API HAL et affiche le texte de la réponse
    Paramètre = requête API HAL"""
    reponse = requests.get(requete_api_hal, timeout=5)
    print(reponse.text)


def afficher_erreur_api(erreur):
    """Affiche les erreurs soulevées lors de l'interrogation de l'API HAL
    Paramètre = erreur"""
    print(f"Les résultats HAL n'ont pas pu être récupérés ({erreur}).")


def afficher_publications_hal(requete_api_hal: str):
    """Interroge l'API HAL et affiche les infos des documents de la réponse
    Paramètre = requête API HAL avec wt=json (str)"""
    try:
        reponse = requests.get(requete_api_hal, timeout=5)
        i = 0
        for doc in reponse.json()['response']['docs']:
            print(i)
            print(f"***\nId = {doc['docid']}\n{soup(doc['label_s'], 'html.parser').text}\n{doc['uri_s']}\n{doc['submitType_s']}\n{doc['docType_s']}\n***\n")
            i += 1
    except requests.exceptions.HTTPError as errh:
        afficher_erreur_api(errh)
    except requests.exceptions.ConnectionError as errc:
        afficher_erreur_api(errc)
    except requests.exceptions.Timeout as errt:
        afficher_erreur_api(errt)
    except requests.exceptions.RequestException as err:
        afficher_erreur_api(err)
    except json.decoder.JSONDecodeError as errj:
        afficher_erreur_api(errj)


url = 'http://api.archives-ouvertes.fr/search/?q=text:"zone atelier alpes"&wt=json&sort=docid asc&fl=docid,label_s,uri_s,submitType_s,docType_s'

afficher_publications_hal(url)