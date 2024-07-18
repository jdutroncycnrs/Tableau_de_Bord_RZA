from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd


def scraping_GN(date):
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

        time.sleep(5)
        current_url = driver.current_url

        with open(f"pages/data/uuids/uuid_cat_InDoRes_{date}.txt","w") as file:
            file.write(current_url)

        m = True

    except Exception as e:
        print(f"Exception occurred: {e}")
        m = False

    driver.quit()
    return m

def recup_group(uuid):
    chrome_options = Options()
    #chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(chrome_options)
    driver.get(f'http://cat.indores.fr/geonetwork/srv/fre/catalog.search#/metadata/{uuid}')

    try:
        accepter_button = driver.find_element(By.CSS_SELECTOR, "p.cookie-warning-actions > button.btn-info").click()
        group = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div/div[2]/div/div/div[3]/div[3]/div/div/div/div[8]/div[2]/div/div[4]/span[3]/strong")      
    except:
        try:
            group = driver.find_element(By.CSS_SELECTOR, "strong.ng-binding:nth-child(2)")
        except:
            try:
                group = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div/div[2]/div/div/div[5]/div[3]/div/div/div/div[9]/div[2]/div/div[4]/span[3]/strong")
            except:
                try:
                    group = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div/div[2]/div/div/div[5]/div[3]/div/div/div/div[8]/div[2]/div/div[4]/span[3]/strong")
                except:
                    try:
                        group = driver.find_element(By.XPATH, "strong.ng-binding:nth-child(1)")
                    except:
                        print('error, aie')

    g = group.text
    driver.quit()
    return g

def uuids_cleaning(date):
    with open(f"pages/data/uuids/uuid_cat_InDoRes_{date}.txt") as file:
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
    df_uuid.to_csv(f"pages/data/uuids/uuid_cat_InDoRes_clean_{date}.csv")

def transcript_json(json_data, file, prefix=""):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, dict) or isinstance(value, list):
                transcript_json(value,file, f"{prefix}.{key}" if prefix else key)
            else:
                #print(f"{prefix}.{key}: {value}" if prefix else f"{key}: {value}")
                file.write(f"{prefix}.{key}:!{value}," if prefix else f"{key}:!{value},")
    elif isinstance(json_data, list):
        for item in json_data:
            transcript_json(item,file, prefix)
    else:
        #print(f"{prefix}: {json_data}" if prefix else f"{json_data}")
        file.write(f"{prefix}:!{json_data}," if prefix else f"{json_data},")