from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QMainWindow
from ui_main import Ui_SubitoBot
import traceback
import json
from bot import startBot
import sys

category_id_map = {
    "Accessori Auto": 5,
    "Accessori Moto": 36,
    "Veicoli commerciali": 4,
    "Informatica": 10,
    "Console e Videogiochi": 44,
    "Audio/Video": 11,
    "Fotografia": 40,
    "Telefonia": 12,
    "Arredamento e Casalinghi": 14,
    "Elettrodomestici": 37,
    "Giardino e Fai da te": 15,
    "Abbigliamento e Accessori": 16,
    "Animali": 23,
    "Musica e Film": 19,
    "Libri e Riviste": 38,
    "Strumenti Musicali": 39,
    "Sports": 20,
    "Biciclette": 41,
    "Collezionismo": 21,
    "Altri": 28
}

class Item(QtWidgets.QFrame):
    def __init__(self, scrollAreaItems, title, image, mainWindow):
        QtWidgets.QFrame.__init__(self, scrollAreaItems)
        self.setMinimumSize(QtCore.QSize(270, 50))
        self.setMaximumSize(QtCore.QSize(270, 50))
        self.setStyleSheet("border: 1px solid #aeb9c6; border-radius: 5px; background-color: rgb(255, 255, 255);")
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("item")
        self.image = QtWidgets.QLabel(self)
        self.image.setGeometry(QtCore.QRect(5, 5, 40, 40))
        self.image.setStyleSheet("border: 0px;")
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap(image))
        self.image.setScaledContents(True)
        self.image.setObjectName("image")
        self.itemName = QtWidgets.QLabel(self)
        self.itemName.setGeometry(QtCore.QRect(60, 15, 205, 20))
        self.itemName.setStyleSheet("border: 0px;")
        self.itemName.setObjectName("itemName")
        self.removeButton = QtWidgets.QPushButton(self)
        self.removeButton.setGeometry(QtCore.QRect(235, 15, 20, 20))
        font = QtGui.QFont()
        font.setFamily("FreeMono")
        font.setBold(True)
        font.setWeight(75)
        self.removeButton.setFont(font)
        self.removeButton.setStyleSheet("border-radius: 10px; border: 0px; background-color: rgb(239, 41, 41); color: rgb(255,255,255)")
        self.removeButton.setObjectName("removeButton")
        self.removeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.removeButton.clicked.connect(self.removeItem)
        self.itemName.setText(title)
        self.removeButton.setText("X")
        self.mainWindow = mainWindow
        self.title = title

    def removeItem(self):
        self.deleteLater()
        self.mainWindow.removeItem(self.title)
        print("Removed item")


class MainWindow(QMainWindow, Ui_SubitoBot):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_SubitoBot.__init__(self)
        self.setupUi(self)

        self.selectImages.clicked.connect(self.openFileNamesDialog)
        self.insertButton.clicked.connect(self.pushConfirmButton)
        self.startButton.clicked.connect(self.startBot)
        self.toDeliver.toggled.connect(self.onDeliverClick)

        self.category.setEditable(True)
        self.category.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.category.lineEdit().setReadOnly(True)

        self.type.setEditable(True)
        self.type.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.type.lineEdit().setReadOnly(True)

        self.gender.setEditable(True)
        self.gender.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.gender.lineEdit().setReadOnly(True)

        self.condition.setEditable(True)
        self.condition.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.condition.lineEdit().setReadOnly(True)

        self.buttonGroup.setId(self.tuttoSubito,0)
        self.buttonGroup.setId(self.deliveryDIY,1)

        self.buttonGroup_2.setId(self.smallSize,10)
        self.buttonGroup_2.setId(self.mediumSize,20)
        self.buttonGroup_2.setId(self.bigSize,30)

        self.items = []
        self.ui_items = []
        self.getJSON()

        self.show()

    def onDeliverClick(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            self.tuttoSubito.setEnabled(True)
            self.deliveryDIY.setEnabled(True)
            self.smallSize.setEnabled(True)
            self.mediumSize.setEnabled(True)
            self.bigSize.setEnabled(True)
            print("delivery enabled")
        else:
            self.tuttoSubito.setEnabled(False)
            self.deliveryDIY.setEnabled(False)
            self.smallSize.setEnabled(False)
            self.mediumSize.setEnabled(False)
            self.bigSize.setEnabled(False)
            print("delivery disabled")

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(QWidget(),"Seleziona le immagini", "","Immagini (*.png *.jpg *.jpeg)", options=options)
        self.flushPreviews()
        self.imageFiles = files
        for filePath in files:
            print(filePath)
            self.addPreview(filePath)

    def flushPreviews(self):
        try:
            for preview in self.previews:
                preview.deleteLater()
        except Exception as e:
            print(e)
        self.previews = []
        print("flushed previews")

    def addPreview(self, filePath):
        preview = QtWidgets.QLabel(self.selectedImagesFrame)
        preview.setMinimumSize(QtCore.QSize(40, 40))
        preview.setMaximumSize(QtCore.QSize(40, 40))
        preview.setText("")
        preview.setPixmap(QtGui.QPixmap(filePath))
        preview.setScaledContents(True)
        preview.setObjectName("preview")
        self.horizontalLayout.insertWidget(1, preview)
        self.previews.append(preview)

    def pushConfirmButton(self):
        try:
            dictFields = {
                "categoria":    category_id_map[self.category.currentText()],
                "tipologia":    self.type.currentIndex()+1,
                "per":          self.gender.currentIndex()+1,
                "condizione":   (self.condition.currentIndex()+1)*10,
                "immagini":     self.imageFiles,
                "titolo":       self.title.text(),
                "descrizione":  self.description.toPlainText(),
                "prezzo":       self.price.text(),
                "dispSped":     self.toDeliver.isChecked(),
                "tipoSped":     self.buttonGroup.checkedId(),
                "dimSped":      self.buttonGroup_2.checkedId(),
                "costoSped":    self.shippingCost.text(),
                "comune":       self.city.text(),
                "indirizzo":    self.address.text(),
                "nascondiIndirizzo": self.addressCheckBox.isChecked(),
                "telefono":     self.phone.text(),
                "nascondiTelefono": self.phoneCheckBox.isChecked()
            }
            self.addItem(dictFields)
            self.items.append(dictFields)
            self.updateJSON()
        except Exception as e:
            print(e)
            traceback.print_exc()

        print("\n".join([str(x) for x in self.items]))


    def addItem(self, dictFields):
        self.ui_items.append(Item(self.scrollAreaItems, dictFields["titolo"], dictFields["immagini"][0], self))
        self.verticalLayout_2.insertWidget(0, self.ui_items[-1], 0, QtCore.Qt.AlignHCenter)
        

    def removeItem(self, title):
        item = None
        try:
            item = next(filter(lambda x: x["titolo"] == title, self.items))
        except Exception as e:
            print(e)

        self.items.remove(item)
        self.updateJSON()
        print("remove " + str(item))

    def updateJSON(self):
        with open('data.json', 'w') as outfile:
            json.dump(self.items, outfile)

    def getJSON(self):
        try:
            with open('data.json', 'r+') as infile:
                self.items = json.load(infile)
        except Exception as e:
            print(e)

        for item in self.items:
            self.addItem(item)

        print("\n".join([str(x) for x in self.items]))

    def startBot(self):
        startBot(self.items)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())