from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

def startBot(dataList):

    username = "cronopowa98@gmail.com"
    password = "m1a9s9s8imo"

    driver = webdriver.Firefox()
    driver.maximize_window()

    driver.delete_all_cookies()
    driver.get("https://areariservata.subito.it/login_form")

    driver.find_element(By.ID, 'didomi-notice-agree-button').click()

    search = driver.find_element(By.ID, "username")
    search.send_keys(username)

    search = driver.find_element(By.ID, "password")
    search.send_keys(password)

    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    for data in dataList:
        driver.get("https://www2.subito.it/aif?subject="+data["titolo"]+"&from=vendere&category=28#insert")
        imagesUploaded = False

        # PAGE1
        while True:
            try:
                chooseFile  = driver.find_element(By.ID, 'fileElem')
                description = driver.find_element(By.ID, 'body')
                price       = driver.find_element(By.ID, 'price')
                city        = driver.find_element(By.ID, 'town')
                address     = driver.find_element(By.ID, 'address')
                hideAddress = driver.find_element(By.NAME, 'map_hidden')
                phone       = driver.find_element(By.ID, 'phone')
                hidePhone   = driver.find_element(By.NAME, 'phone_hidden')
                submitBtn   = driver.find_element(By.ID, 'btnAiSubmit')

                if not imagesUploaded:
                    chooseFile.send_keys("\n".join(data["immagini"]))
                    imagesUploaded = True
                description.clear()
                description.send_keys(data["descrizione"])
                price.clear()
                price.send_keys(data["prezzo"])
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

                submitBtn.click()
            except Exception as e:
                print(str(e))
                sleep(0.1)
                continue
            break

        sleep(6)
        continue

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

