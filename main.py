from selenium import webdriver
import chromedriver_autoinstaller
from tkinter.filedialog import askopenfilenames
import json
import os
import sys
import shutil

from utils import *

filepath_items = r'resources\items.json'
filepath_template = r'resources\template.json'

def publish():
    with open(filepath_items) as f:
        items = json.load(f)
    
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.delete_all_cookies()

    cwd = os.getcwd()
    login(driver)
    input('continue?')
    for data in items:
        data['immagini'] = [os.path.join(cwd, p) for p in data['immagini']]
        page1(driver, data)
        page2(driver)

    sleep(5)
    driver.quit()

def create_new_adv():
    with open(filepath_items) as f:
        items = json.load(f)

    with open(filepath_template) as f:
        template = json.load(f)

    for key in template.keys():
        OK  = False
        while not OK:
            try:
                value = ''
                if key == 'id':
                    value = input(key + ' (unique)?: ').lower()
                elif key == 'categoria':
                    print('OPTIONS:', '\n'.join([f'{k:<5}: {v}' for k, v in CATEGORIES.items()]), sep='\n')
                    value = int(input(f'{key}? '))
                    assert value in CATEGORIES
                elif key == 'tipologia':
                    options = TYPES[CATEGORIES[template['categoria']]]
                    if len(options) > 0:
                        print('OPTIONS:', '\n'.join([f'{id:<5}: {t}' for id, t in enumerate(options)]), sep='\n')
                        value = int(input(f'{key}? '))
                        value = value + 1
                    else:
                        value = 1
                elif key == 'immagini':
                    paths = askopenfilenames()
                    relpath = os.path.join('resources', template['id'])
                    os.makedirs(relpath)
                    paths_new = [os.path.join(relpath, f'{id}{os.path.splitext(p)[1]}') for id, p in enumerate(paths)]
                    for src, dst in zip(paths, paths_new):
                        shutil.copyfile(src, dst)
                    value = paths_new
                elif key == 'tipo_di_annuncio':
                    options = ['Regalo', 'Vendita']
                    print('OPTIONS:', '\n'.join([f'{id:<5}: {t}' for id, t in enumerate(options)]), sep='\n')
                    value = int(input(f'{key}? '))
                    value = options[value]
                elif key == 'condizione':
                    options = ['Nuovo', 'ComeNuovo', 'Ottimo', 'Buono', 'Danneggiato']
                    print('OPTIONS:', '\n'.join([f'{id:<5}: {t}' for id, t in enumerate(options)]), sep='\n')
                    value = int(input(f'{key}? '))
                    value = options[value]
                elif key == 'spedizione':
                    options = ['Nessuna', 'TuttoSubito', 'GestitaDaTe']
                    print('OPTIONS:', '\n'.join([f'{id:<5}: {t}' for id, t in enumerate(options)]), sep='\n')
                    value = input(f'{key}? ')
                    if value == '':
                        value = options[0]
                    else:
                        value = options[int(value)]
                elif key == 'dimensioni':
                    if template['spedizione'] == 'TuttoSubito':
                        options = ['Piccolo', 'Medio', 'Grande', 'Maxi']
                        print('OPTIONS:', '\n'.join([f'{id:<5}: {t}' for id, t in enumerate(options)]), sep='\n')
                        value = int(input(f'{key}? '))
                        value = options[value]
                elif key == 'costi_di_spedizione':
                    if template['spedizione'] == 'GestitaDaTe':
                        value = input(f'{key}? ')
                elif key == 'nascondi_numero':
                    value = True
                elif key == 'inserzionista':
                    value = 'Privato'
                else:
                    value = input(f'{key} (default: {template[key]})? ')
                    if value == '':
                        value =  template[key]

                template[key] = value
                OK  = True
            except Exception as e:
                print(e)

    # remove duplated ids
    items = [x for x in items if x['id'] != template['id']]
    items.append(template)

    with open(filepath_items, 'w') as f:
        json.dump(items, f, indent=2)

def list_advs():
    with open(filepath_items) as f:
        items = json.load(f)

    for idx, item in enumerate(items):
        print(f'{idx :<3}: {item['id']}')
    
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'add':
        create_new_adv()
    elif len(sys.argv) > 1 and sys.argv[1].lower() == 'list':
        list_advs()
    else:
        publish()
