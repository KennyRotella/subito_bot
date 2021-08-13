import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

cwd = os.getcwd()
dirs = list(os.walk(cwd))[0][1]

driver = webdriver.Chrome()
driver.implicitly_wait(10)

for dir in dirs:
    images = []
    for file in os.listdir(dir):
        if file.endswith(".jpg"):
            images.append(os.path.join(cwd, dir, file))

    f = open(os.path.join(dir,'data.json'),)
    data = json.load(f)

    driver.delete_all_cookies()
    driver.get("https://www2.subito.it/aif?subject="+data["title"]+"&from=vendere&category="+data["category"]+"&type="+data["type"]+"#insert")

    search = driver.find_element_by_name("username")
    search.send_keys(data["username"])

    search = driver.find_element_by_name("password")
    search.send_keys(data["password"])

    search.send_keys(Keys.RETURN)
    sleep(2)

    driver.execute_script("document.querySelector('#aiform > div.container.step_0 > div.rowNode.optim-item_shippable > div.boxInput.lfloat > div:nth-child(1) > input[type=checkbox]').click()")
    driver.execute_script("document.querySelector('#aiform > div.container.step_1 > div.rowNode.optim-phone_hidden > div.boxInput.lfloat > div:nth-child(1) > input[type=checkbox]').click()")

    chooseFile = driver.find_element_by_id('fileElem')

    char = "\n"
    chooseFile.send_keys(char.join(images))
    sleep(2)

    description = driver.find_element_by_id('body')
    description.send_keys(data["description"])

    price = driver.find_element_by_id('price')
    price.send_keys(data["price"])

    city = driver.find_element_by_id('town')
    city.clear()
    city.send_keys(data["city"])

    name = driver.find_element_by_id('name')
    name.clear()
    name.send_keys(data["name"])

    phone = driver.find_element_by_id('phone')
    phone.clear()
    phone.send_keys(data["phone"])

    phone.send_keys(Keys.RETURN)

    sleep(8)
    confirm = driver.find_element_by_id('btnConfirm')
    confirm.send_keys(Keys.RETURN)

    sleep(5)
    driver.get("https://areariservata.subito.it/logout")

driver.quit()
