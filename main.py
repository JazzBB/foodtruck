import requests
import json
import objectpath
from py_translator import Translator
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QHBoxLayout, QLabel, QComboBox, QDialog
from PyQt5.QtCore import QTimer, Qt, QPoint, QObject
import sys

APPID = ""
KULCS = ""

class FoodTruck(QtWidgets.QMainWindow):
    def lekerdezes(self):
        index_from = randint(1,20)
        index_to = index_from + 1
        #recept_out törlése
        self.recept_out.clear()
        #husok ellenörzése
        if self.marha.isChecked() == True:
            hus = 'beef'
        if self.csirke.isChecked() ==  True:
            hus = 'chicken'
        if self.sertes.isChecked() == True:
            hus = 'pork'
        if self.hal.isChecked() == True:
            hus = 'fish'
        if self.pulyka.isChecked() == True:
            hus = 'turkey'
        print(hus)
        response = requests.get("https://api.edamam.com/search?q="+hus+"+oregano&app_id="+APPID+"&app_key="+KULCS+"&from="+str(index_from)+"&to="+str(index_to)+"&diet=low-carb&nutrients%5BCHOCDF%5D=45-50")
        response = response.json()
        #parsed_response = json.loads(response)
        #Adatok kiszedése a JSONbol
        response_tree = objectpath.Tree(response['hits'])
        szenhidrat = tuple(response_tree.execute('$..CHOCDF'))
        if len(szenhidrat) == 0:
            print('A keresési feltételeknek nincs megfelelő recept')
            exit
        else:
            szemely = tuple(response_tree.execute('$..yield'))
            recept_neve = tuple(response_tree.execute('$..label'))
            hozzavalok = tuple(response_tree.execute('$..ingredients'))
            fozesi_ido = tuple(response_tree.execute('$..totalTime'))
            kaloria = tuple(response_tree.execute('$..ENERC_KCAL'))
            #print, aztan majd megy GUIra
            self.receptcime.setText(recept_neve[0])
            print(szemely[0])
            print("Össz szénhidrát tartalom:"+ str(szenhidrat[0]['quantity'])+ str(szenhidrat[0]['unit']))
            egy_adag_ch = int(szenhidrat[0]['quantity'])/int(szemely[0])
            print("Egy adag szénhidrát tartalma: "+str(egy_adag_ch))
            print("Össz kalória tartalom: "+str(kaloria[0]['quantity'])+ str(kaloria[0]['unit']))
            print("Főzési idő: "+str(fozesi_ido[0]))
            print("Hozzávalók\n----------------------------------------------------------------")
            for hozzavalok_db in hozzavalok:
               self.recept_out.append(Translator().translate(text=hozzavalok_db['text'],dest='hu').text)
        return
    def mentes(self):
        with open(self.receptcime.text()+'.txt', 'w') as recept_text:
            recept_text.write(str(self.recept_out.toPlainText()))

    def __init__(self):
        super(FoodTruck,self).__init__()
        uic.loadUi('main.ui',self)
        self.recept_keres.clicked.connect(self.lekerdezes)
        self.recept_mentes.clicked.connect(self.mentes)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FoodTruck()
    window.show()
    sys.exit(app.exec_())

main()
