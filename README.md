# Subito Bot

## About The Project
[![Subito Bot Screen Shot][product-screenshot]](https://example.com)

This project helps to speed-up insertion and filling of advertisments on the website [Subito.it](https://www.subito.it/)

### Built With
* [Selenium](https://www.selenium.dev/)
* [PyQt](https://www.qt.io/)
* [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/)

## Getting Started
### Prerequisites
1. ***Important*** These portables are built for chrome version 99, check your version (chrome://settings/help)
2. Download the portable package based on your OS [Windows] or [Linux](https://github.com/KennyRotella/subito_bot/blob/main/portable_builds/LinuxBuild.zip)
3. Edit `Credenziali.ini` with your credentials under [credenziali] section
4. Insert all information needed for your advertisment (there may be more fields in the GUI than needed)
5. Once filled all fields click on the red button "Inserisci annuncio", do this for every advertisment
6. Once all your advertisments are inserted click on the blue button "Avvia BOT"
7. Enjoy! (Hopefully)

### Build from source on Linux
1. Clone the repo
```sh
   git clone https://github.com/KennyRotella/subito_bot.git
   cd subito_bot
```
2. Installing dependencies
```sh
   pip install -r requirements.txt
```
3. Build GUI python files
```sh
   pyuic5 GUI/ui_main.ui -o ui_main.py
   pyrcc5 GUI/test.qrc -o test_rc.py
```
4. Downloading chromedriver
- Download the latest release of chrome driver [here](https://chromedriver.chromium.org/downloads) based on your Chrome browser version (chrome://settings/help)
- Place your downloaded `chromedriver.exe` into a folder called `driver`
5. Making a .spec file for PyInstaller
- Linux
```sh
   pyi-makespec main.py --onefile --noconsole --add-binary "driver/chromedriver:driver/" --add-data "Credenziali.ini:." --name subito-bot
```
- Windows
```sh
   pyi-makespec main.py --onefile --noconsole --add-binary "driver\chromedriver.exe;driver\" --add-data "Credenziali.ini;." --name subito-bot
```
6. Run pyinstaller command
```sh
   pyinstaller --clean subito-bot.spec
```
- You may find the exe inside the dist folder. Run the subito-bot.exe to try it out
- Modify the `Credenziali.ini` with your credentials and put it inside the same executable folder
- This [guide](https://medium.com/technology-hits/easily-distribute-python-selenium-applications-with-pyinstaller-ef276844ad2d) was used for packaging
