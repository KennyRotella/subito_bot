from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from configparser import ConfigParser
import traceback
import os
import sys

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def insertImages(driver, data):
    chooseFile  = driver.find_element(By.ID, 'fileElem')
    chooseFile.send_keys("\n".join(data["immagini"]))

def insertData(driver, data):
    clothing_gender             = driver.find_elements(By.NAME,'clothing_gender')
    item_condition              = driver.find_elements(By.NAME,'item_condition')
    description                 = driver.find_element(By.ID, 'body')
    price                       = driver.find_element(By.ID, 'price')
    item_shippable              = driver.find_elements(By.XPATH,"//input[@name='item_shippable']")
    city                        = driver.find_element(By.ID, 'town')
    address                     = driver.find_element(By.ID, 'address')
    hideAddress                 = driver.find_element(By.NAME, 'map_hidden')
    phone                       = driver.find_element(By.ID, 'phone')
    hidePhone                   = driver.find_element(By.NAME, 'phone_hidden')

    if len(clothing_gender) == 1:
        Select(clothing_gender[0]).select_by_value(str(data["per"]))
    if len(item_condition) == 1:
        Select(item_condition[0]).select_by_value(str(data["condizione"]))
    description.clear()
    description.send_keys(data["descrizione"])
    price.clear()
    price.send_keys(data["prezzo"])
    if len(item_shippable) and data["dispSped"]:
        item_shippable = item_shippable[0]
        if not item_shippable.is_selected():
            item_shippable.click()
        item_shipping_type = driver.find_element(By.XPATH,"//input[@name='item_shipping_type'][@value='"+str(data["tipoSped"])+"']")
        item_shipping_type.click()
        if data["tipoSped"] == 1:
            item_shipping_cost = driver.find_element(By.XPATH,"//input[@name='item_shipping_cost']")
            item_shipping_cost.clear()
            item_shipping_cost.send_keys(data["costoSped"])
        else:
            item_shipping_package_size = driver.find_element(By.XPATH,"//input[@name='item_shipping_package_size'][@value='"+str(data["dimSped"])+"']")
            item_shipping_package_size.click()
    city.clear()
    city.send_keys(data["comune"])
    address.clear()
    address.send_keys(data["indirizzo"])

    if data["nascondiIndirizzo"]:
        hideAddress.click()
    
    phone.clear()
    phone.send_keys(data["telefono"])

    if data["nascondiTelefono"]:
        hidePhone.click()


def startBot(dataList):
    # read init file
    config = ConfigParser()
    config.read("credenziali.ini")
    EMAIL = config.get("credenziali", "email")
    PASSWORD = config.get("credenziali", "password")
    CHROME_DRIVER_PATH = config.get("chromedriver", "path")

    driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH))
    driver.maximize_window()

    driver.delete_all_cookies()
    driver.get("https://areariservata.subito.it/login_form")

    driver.find_element(By.ID, 'didomi-notice-agree-button').click()

    search = driver.find_element(By.ID, "username")
    search.send_keys(EMAIL)

    search = driver.find_element(By.ID, "password")
    search.send_keys(PASSWORD)

    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    sleep(2)

    for data in dataList:
        driver.get("https://www2.subito.it/aif?subject="+data["titolo"]+"&category="+str(data["categoria"])+"&type="+str(data["tipologia"])+"&from=vendere#insert")

        # PAGE1
        while True:
            try:
                insertImages(driver, data)
            except Exception as e:
                print(str(e))
                sleep(0.1)
                continue
            break
        
        while True:
            try:
                insertData(driver, data)
                submitBtn   = driver.find_element(By.ID, 'btnAiSubmit')
                submitBtn.click()
            except Exception as e:
                print(str(e))
                traceback.print_exc()
                sleep(0.1)
                continue
            break

        # PAGE2
        while True:
            try:
                driver.find_element(By.ID, 'btnConfirm').click()
            except Exception as e:
                print(str(e))
                sleep(0.1)
                continue
            break

        # PAGE3
        while True:
            try:
                if driver.current_url != "https://areariservata.subito.it/annunci/esito-inserimento":
                    driver.find_element(By.XPATH, '//form/div[5]/button').click()
                assert driver.current_url == "https://areariservata.subito.it/annunci/esito-inserimento" 
            except Exception as e:
                print(str(e))
                sleep(0.1)
                continue
            break

        sleep(1)
    driver.quit()

