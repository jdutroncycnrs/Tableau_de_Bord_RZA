from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd


def scraping_GN():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(chrome_options)
    driver.get('https://cat.indores.fr/geonetwork/srv/fre/catalog.search#/search?any=')

    try:

        accepter_button = driver.find_element(By.CSS_SELECTOR, "p.cookie-warning-actions > button.btn-info").click()

        dropdown_toggle = driver.find_element(By.XPATH, "//button[@class='btn btn-default dropdown-toggle']").click()

        tout_selectionner_link = driver.find_element(By.XPATH, "//a[@data-ng-click='selectAll()']").click()

        parent_div_xpath = "//div[@class='btn-group gn-selection-actions ng-scope']"
        dropdown_toggle_xpath = f"{parent_div_xpath}//button[@class='btn btn-default dropdown-toggle']"
        dropdown_toggle = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, dropdown_toggle_xpath)))
        dropdown_toggle.click()

        uniquement_la_selection_xpath = f"//a[contains(., 'Uniquement la sélection')]"
        uniquement_la_selection = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, uniquement_la_selection_xpath)))
        uniquement_la_selection.click()

    except Exception as e:
        print(f"Exception occurred: {e}")

    time.sleep(5)
    current_url = driver.current_url

    with open("pages/data/uuid_cat_InDoRes.txt","w") as file:
        file.write(current_url)

    m = "la Récup est OK"

    driver.quit()

    return m

def uuids_cleaning():
    with open(f"pages/data/uuid_cat_InDoRes.txt") as file:
        t = file.read()
    t2 =t[70:]
    list_uuid_brutes= re.split(',', t2)
    new_list_uuid = []
    for i in range(1,len(list_uuid_brutes)):
        if "oai:search-data.ubfc.fr:" in list_uuid_brutes[i]:
            new_list_uuid.append(list_uuid_brutes[i].replace("oai:search-data.ubfc.fr:",''))
        elif "urn:isogeo:metadata:uuid:" in list_uuid_brutes[i]:
            new_list_uuid.append(list_uuid_brutes[i].replace("urn:isogeo:metadata:uuid:",''))
        else:
            try:
                new_list_uuid.append(re.split('%22', list_uuid_brutes[i])[1])
            except:
                new_list_uuid.append(list_uuid_brutes[i])
    new_list_uuid2 = []            
    for j in range(0,len(new_list_uuid)):
        try:
            new_list_uuid2.append(re.split('%22', new_list_uuid[j])[1])
        except:
            new_list_uuid2.append(new_list_uuid[j])
    df_uuid = pd.DataFrame(data= new_list_uuid2,columns=["uuid_cat_InDoRes"])
    df_uuid.to_csv(f"pages/data/uuid_cat_InDoRes_clean.csv")
    m2 = "Cleaning ok"
    return m2