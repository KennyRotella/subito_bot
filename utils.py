from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from difflib import SequenceMatcher
import json

CATEGORIES = {
    2: "Auto",
    5: "Accessori Auto",
    3: "Moto e Scooter",
    36: "Accessori Moto",
    22: "Nautica",
    34: "Caravan e Camper",
    4: "Veicoli commerciali",
    1: "Tutto motori",
    9: "Elettronica",
    10: "Informatica",
    44: "Console e Videogiochi",
    11: "Audio/Video",
    40: "Fotografia",
    12: "Telefonia",
    13: "Per la casa e la persona",
    14: "Arredamento e Casalinghi",
    37: "Elettrodomestici",
    15: "Giardino e Fai da te",
    16: "Abbigliamento e Accessori",
    17: "Tutto per i bambini",
    18: "Sports e hobby",
    23: "Animali",
    100: "Accessori per animali",
    19: "Musica e Film",
    38: "Libri e Riviste",
    39: "Strumenti Musicali",
    20: "Sports",
    41: "Biciclette",
    21: "Collezionismo",
    28: "Altri",
    7: "Appartamenti",
    43: "Camere/Posti letto",
    29: "Ville singole e a schiera",
    30: "Terreni e rustici",
    31: "Garage e box",
    32: "Loft, mansarde e altro",
    33: "Case vacanza",
    8: "Uffici e Locali commerciali",
    6: "Tutto immobili",
    26: "Offerte di lavoro",
    50: "Servizi",
    42: "Candidati in cerca di lavoro",
    25: "Attrezzature di lavoro",
    24: "Tutto lavoro"
}

TYPES = {
    'Auto': [], 
    'Accessori Auto': [], 
    'Moto e Scooter': [], 
    'Accessori Moto': [], 
    'Nautica': [], 
    'Caravan e Camper': [], 
    'Veicoli commerciali': [], 
    'Tutto motori': [], 
    'Elettronica': [], 
    'Informatica': ['NoteBook & Tablet', 'Computer Fissi', 'Accessori'], 
    'Console e Videogiochi': [], 
    'Audio/Video': ['TV', 'Lettori DVD', 'Radio/Stereo', 'Lettori MP3', 'Altro'], 
    'Fotografia': [], 
    'Telefonia': ['Cellulari e Smartphone', 'Accessori Telefonia', 'Fissi, Cordless e Altro'], 
    'Per la casa e la persona': [], 
    'Arredamento e Casalinghi': [], 
    'Elettrodomestici': [], 
    'Giardino e Fai da te': [], 
    'Abbigliamento e Accessori': ['Scarpe', 'Borse', 'Orologi e Gioielli', 'Polo e t-shirt', 'Pantaloni', 'Gonne', 'Felpe e maglioni', 'Giacche e giubbotti', 'Vestiti completi', 'Intimo', 'Accessori', 'Altro'], 
    'Tutto per i bambini': ['Abbigliamento Bimbi', "Prodotti per l'infanzia", 'Giochi'], 
    'Sports e hobby': [], 
    'Animali': [], 
    'Accessori per animali': [], 
    'Musica e Film': [], 
    'Libri e Riviste': ['Letteratura e Narrativa', 'Gialli e Thriller', 'Biografie', 'Storia', 'Cucina', 'Fumetti', 'Libri per bambini', 'Libri scolastici e universitari', 'Altro'], 
    'Strumenti Musicali': [], 
    'Sports': ['Calcio', 'Palestra', 'Basket', 'Volley', 'Sci e Snowboard', 'Ciclismo', 'Acquatici', 'Golf', 'Motori', 'Outdoor', 'Altro'], 
    'Biciclette': ['Uomo', 'Donna', 'Bimbo', 'MTB e Touring', 'Corsa', 'Pieghevoli', 'BMX', 'Scatto fisso e single speed', 'Componenti e abbigliamento', 'Altre tipologie'], 
    'Collezionismo': ['Francobolli', 'Monete', 'Editoria', 'Carte e Schede', 'Modellismo', 'Cartoline', 'Militaria', 'Modernariato', 'Bambole', 'Altro'], 
    'Altri': [], 
    'Appartamenti': [], 
    'Camere/Posti letto': [], 
    'Ville singole e a schiera': [], 
    'Terreni e rustici': [], 
    'Garage e box': [], 
    'Loft, mansarde e altro': [], 
    'Case vacanza': [], 
    'Uffici e Locali commerciali': [], 
    'Tutto immobili': [], 
    'Offerte di lavoro': [], 
    'Servizi': [], 
    'Candidati in cerca di lavoro': [], 
    'Attrezzature di lavoro': [], 
    'Tutto lavoro': []
}

GUI = {
    # LOGIN
    'accetta':                lambda d: d.find_element(By.ID, 'didomi-notice-agree-button'),
    'email':                  lambda d: d.find_element(By.ID, 'username'),
    'password':               lambda d: d.find_element(By.ID, 'password'),
    'accedi':                 lambda d: d.find_elements(By.XPATH, '//button[@type="submit"]')[0],
    'i_tuoi_annunci':         lambda d: d.find_elements(By.XPATH, '//*[@id="__next"]/div/main/div[2]/ul/li[1]/a/span')[0], 

    # PAGE1
    'immagini':                 lambda d: d.find_element(By.ID, 'file-input'),
    'tipo_di_annuncio_Vendita': lambda d: d.find_elements_by_xpath('//label[text()="In vendita"]')[0],
    'tipo_di_annuncio_Regalo':  lambda d: d.find_elements_by_xpath('//label[text()="In regalo"]')[0],
    'titolo':                   lambda d: d.find_element(By.ID, 'title'),
    'descrizione':              lambda d: d.find_element(By.ID, 'description'),
    'comune':                   lambda d: d.find_element(By.ID, 'location'),
    'condizione':               lambda d: d.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/form/div/section[5]/div[2]/div/div/div/div')[0],
    'condizione_Nuovo':         lambda d: d.find_elements_by_xpath('//*[@id="itemCondition__option--0"]')[0],
    'condizione_ComeNuovo':     lambda d: d.find_elements_by_xpath('//*[@id="itemCondition__option--1"]')[0],
    'condizione_Ottimo':        lambda d: d.find_elements_by_xpath('//*[@id="itemCondition__option--2"]')[0],
    'condizione_Buono':         lambda d: d.find_elements_by_xpath('//*[@id="itemCondition__option--3"]')[0],
    'condizione_Danneggiato':   lambda d: d.find_elements_by_xpath('//*[@id="itemCondition__option--4"]')[0],
    'prezzo':                   lambda d: d.find_element(By.ID, 'price'),
    'spedizione':               lambda d: d.find_element(By.ID, 'itemShippable'),
    'spedizione_TuttoSubito':   lambda d: d.find_elements_by_xpath('//label[@aria-label="Spedizione con TuttoSubito"]/div[@class="ListItemRadio_radio__eriFK"]')[0],
    'spedizione_Piccolo':       lambda d: d.find_elements_by_xpath('//label[@aria-label="Piccolo (Massimo 2kg)"]')[0],
    'spedizione_Medio':         lambda d: d.find_elements_by_xpath('//label[@aria-label="Medio (Massimo 5kg)"]')[0],
    'spedizione_Grande':        lambda d: d.find_elements_by_xpath('//label[@aria-label="Grande (Massimo 15kg)"]')[0],
    'spedizione_Maxi':          lambda d: d.find_elements_by_xpath('//label[@aria-label="Maxi (Massimo 20kg)"]')[0],
    'spedizione_GestitaDaTe':   lambda d: d.find_elements_by_xpath('//label[@aria-label="Spedizione gestita da te (pacchi ingombranti)"]/div[@class="ListItemRadio_radio__eriFK"]')[0],
    'costi_di_spedizione':      lambda d: d.find_element(By.ID, 'itemShippingCost'),
    'telefono':                 lambda d: d.find_element(By.ID, 'phone'),
    'nascondi_numero':          lambda d: d.find_element(By.ID, 'phoneHidden'),
    'inserzionista_Privato':    lambda d: d.find_elements_by_xpath('//label[text()="Privato"]')[0],
    'inserzionista_Azienda':    lambda d: d.find_elements_by_xpath('//label[text()="Azienda"]')[0],
    'continua':                 lambda d: d.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/form/section/button')[0],

    # PAGE2
    'pubblica_annuncio':        lambda d: d.find_elements_by_xpath('//span[text()="Pubblica annuncio"]')[0],
}

def get_gui(driver, name, retry=10):
    count = 0
    while count < retry:
        sleep(0.5)
        count += 1
        try:
            return GUI[name](driver)
        except:
            pass
    
def type_text(driver, name, text):
    ui = get_gui(driver, name)
    # check string similarity
    while SequenceMatcher(None, ui.get_attribute("value").strip().lower(), text.strip().lower()).ratio() < 0.8:
        ui.click()
        ui.clear()
        ui.send_keys(text)
        sleep(1)

def login(driver):

    # read credentials
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)

    driver.get('https://areariservata.subito.it/login_form')
    get_gui(driver, 'accetta').click()
    type_text(driver, 'email', credentials['EMAIL'])
    type_text(driver, 'password', credentials['PASSWORD'])
    get_gui(driver, 'accedi').click()

def page1(driver, data):
    get_gui(driver, 'i_tuoi_annunci')
    driver.get(f'https://inserimento.subito.it/?category={str(data["categoria"])}&type={str(data["tipologia"])}&from=vendere#insert')

    get_gui(driver, 'immagini').send_keys('\n'.join(data['immagini']))
    get_gui(driver, f'tipo_di_annuncio_{data["tipo_di_annuncio"]}').click()
    
    type_text(driver, 'titolo', data['titolo'])
    type_text(driver, 'descrizione', data['descrizione'])
    get_gui(driver, 'condizione').click()
    get_gui(driver, f'condizione_{data["condizione"]}').click()
    type_text(driver, 'comune', data['comune'])
    get_gui(driver, 'comune').send_keys(Keys.RETURN)

    if data['prezzo'] is None:
        get_gui(driver, 'prezzo').clear()
    else:
        type_text(driver, 'prezzo', data['prezzo'])
    
    if data['spedizione'] == 'TuttoSubito':
        get_gui(driver, 'spedizione_TuttoSubito').click()
        get_gui(driver, f'spedizione_{data["dimensioni"]}').click()
    elif data['spedizione'] == 'GestitaDaTe':
        get_gui(driver, 'spedizione_GestitaDaTe').click()
        type_text(driver, 'costi_di_spedizione', data['costi_di_spedizione'])
    else:
        get_gui(driver, 'spedizione').click()
        
    type_text(driver, 'telefono', data['telefono'])
    nascondi_numero_checked = get_gui(driver, 'nascondi_numero').get_attribute('data-state') == 'checked'
    if nascondi_numero_checked and not data['nascondi_numero'] or not nascondi_numero_checked and data['nascondi_numero']:
        get_gui(driver, 'nascondi_numero').click()

    # get_gui(driver, f'inserzionista_{data['inserzionista']}').click()
    
    get_gui(driver, 'continua').click()

def page2(driver):
    get_gui(driver, 'pubblica_annuncio').click()