import requests
import json
import objectpath
from py_translator import Translator
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QHBoxLayout, QLabel, QComboBox, QDialog
from PyQt5.QtCore import QTimer, Qt, QPoint, QObject
import sys

APPID = 
KULCS = 
check_box_value = 1
zoldsegek = ['hagyma','krumpli','batáta','paradicsom','zeller','répa','karalábé','saláta','káposzta','cukkini','padlizsán','uborka','paprika','karfiol']
fuszerek  = ['Bazsalikom','Petrezselyem','Oregánó','Fahéj','Dió','Szerecsendió','Chili','Kakukkfű','Koriander','Tárkony']
gyumolcsok= ['alma','Narancs','Körte','Citrom','Ananász','Meggy','Cseresznye','Lime','Szilva','Barack']

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
        #zöldségek ellenörzése
        zoldseg = ''
        gyumolcs = ''
        gyindex = 0
        for zoldsegek_db in zoldsegek:
            checkbox_nr = zoldsegek.index(zoldsegek_db)+1
            command = "self.checkBox_"+str(checkbox_nr)+".isChecked()"
            if eval(command) == True:
                zoldseg = zoldseg + "+" + str(Translator().translate(text=zoldsegek[checkbox_nr-1],dest='en').text)
        for gyumolcsok_db in gyumolcsok:
            checkbox_nr_gyumolcs = gyumolcsok.index(gyumolcsok_db)+26
            command = "self.checkBox_"+str(checkbox_nr_gyumolcs)+".isChecked()"
            if eval(command) == True:
                gyumolcs = gyumolcs + "+" + str(Translator().translate(text=gyumolcsok[checkbox_nr_gyumolcs-26],dest='en',src='hu').text)
        response = requests.get("https://api.edamam.com/search?q="+hus+zoldseg+gyumolcs+"&app_id="+APPID+"&app_key="+KULCS+"&from="+str(index_from)+"&to="+str(index_to)+"&diet=low-carb&nutrients%5BCHOCDF%5D=45-50")
        response = response.json()
        print(hus,zoldseg,gyumolcs)
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
            cukor = tuple(response_tree.execute('$..SUGAR'))
            #zsirok
            zsir  = tuple(response_tree.execute('$..FAT'))
            telitett_zsir = tuple(response_tree.execute('$..FASAT'))
            transz_zsir = tuple(response_tree.execute('$..FATRN'))
            egyszeresen_tel_zsir = tuple(response_tree.execute('$..FAMS'))
            tobbszoros_tel_zsir  = tuple(response_tree.execute('$..FAPU'))
            #ásványianyagok
            natrium =   tuple(response_tree.execute('$..NA'))
            magnezium = tuple(response_tree.execute('$..MG'))
            kalcium =   tuple(response_tree.execute('$..CA'))
            kalium  =   tuple(response_tree.execute('$..K'))
            vas =       tuple(response_tree.execute('$..FE'))
            cink =      tuple(response_tree.execute('$..ZN'))
            foszfor =   tuple(response_tree.execute('$..P'))
            #vitaminok
            avitamin = tuple(response_tree.execute('$..VITA_RAE'))
            cvitamin = tuple(response_tree.execute('$..VITC'))
            b1vitamin= tuple(response_tree.execute('$..THIA'))
            b2vitamin= tuple(response_tree.execute('$..RIBF'))
            b3vitamin= tuple(response_tree.execute('$..NIA'))
            b6vitamin= tuple(response_tree.execute('$..VITB6A'))
            b12vitamin=tuple(response_tree.execute('$..VITB12'))
            dvitamin=  tuple(response_tree.execute('$..VITD'))
            evitamin=  tuple(response_tree.execute('$..TOCPHA'))
            kvitamin=  tuple(response_tree.execute('$..VITK1'))

            #print, aztan majd megy GUIra
            self.receptcime.setText(recept_neve[0])
            #Tápanyagok fül
            #Szénhidrátok
            self.ossz_ch.setText(str(round(int(szenhidrat[0]['quantity']),2))+ str(szenhidrat[0]['unit']))
            self.egy_ch.setText(str(round(int(szenhidrat[0]['quantity'])/int(szemely[0]),2))+ str(szenhidrat[0]['unit']))
            self.ossz_cukor.setText(str(round(int(cukor[0]['quantity']),2))+ str(cukor[0]['unit']))
            self.egy_cukor.setText(str(round(int(cukor[0]['quantity'])/int(szemely[0]),2))+ str(cukor[0]['unit']))
            #zsírok
            self.egy_zsir.setText(str(round(int(zsir[0]['quantity'])/int(szemely[0]),2))+ str(zsir[0]['unit']))
            self.egy_telitett.setText(str(round(int(telitett_zsir[0]['quantity'])/int(szemely[0]),2))+ str(telitett_zsir[0]['unit']))
            self.egy_transz.setText(str(round(int(transz_zsir[0]['quantity'])/int(szemely[0]),2))+ str(transz_zsir[0]['unit']))
            self.egy_egyszer.setText(str(round(int(egyszeresen_tel_zsir[0]['quantity'])/int(szemely[0]),2))+ str(egyszeresen_tel_zsir[0]['unit']))
            self.egy_tobbszor.setText(str(round(int(tobbszoros_tel_zsir[0]['quantity'])/int(szemely[0]),2))+ str(tobbszoros_tel_zsir[0]['unit']))
            #ásványi anyagok
            self.na.setText(str(round(int(natrium[0]['quantity'])/int(szemely[0]),2))+ str(natrium[0]['unit']))
            self.mg.setText(str(round(int(magnezium[0]['quantity'])/int(szemely[0]),2))+ str(magnezium[0]['unit']))
            self.ca.setText(str(round(int(kalcium[0]['quantity'])/int(szemely[0]),2))+ str(kalcium[0]['unit']))
            self.ka.setText(str(round(int(kalium[0]['quantity'])/int(szemely[0]),2))+ str(kalium[0]['unit']))
            self.fe.setText(str(round(int(vas[0]['quantity'])/int(szemely[0]),2))+ str(vas[0]['unit']))
            self.zn.setText(str(round(int(cink[0]['quantity'])/int(szemely[0]),2))+ str(cink[0]['unit']))
            self.po.setText(str(round(int(foszfor[0]['quantity'])/int(szemely[0]),2))+ str(foszfor[0]['unit']))
            #vitaminok
            self.avit.setText(str(round(int(avitamin[0]['quantity'])/int(szemely[0]),2))+ str(avitamin[0]['unit']))
            self.cvit.setText(str(round(int(cvitamin[0]['quantity'])/int(szemely[0]),2))+ str(cvitamin[0]['unit']))
            self.b1vit.setText(str(round(int(b1vitamin[0]['quantity'])/int(szemely[0]),2))+ str(b1vitamin[0]['unit']))
            self.b2vit.setText(str(round(int(b2vitamin[0]['quantity'])/int(szemely[0]),2))+ str(b2vitamin[0]['unit']))
            self.b3vit.setText(str(round(int(b3vitamin[0]['quantity'])/int(szemely[0]),2))+ str(b3vitamin[0]['unit']))
            self.b6vit.setText(str(round(int(b6vitamin[0]['quantity'])/int(szemely[0]),2))+ str(b6vitamin[0]['unit']))
            self.b12vit.setText(str(round(int(b12vitamin[0]['quantity'])/int(szemely[0]),2))+ str(b12vitamin[0]['unit']))
            self.dvit.setText(str(round(int(dvitamin[0]['quantity'])/int(szemely[0]),2))+ str(dvitamin[0]['unit']))
            self.evit.setText(str(round(int(evitamin[0]['quantity'])/int(szemely[0]),2))+ str(evitamin[0]['unit']))
            self.kvit.setText(str(round(int(kvitamin[0]['quantity'])/int(szemely[0]),2))+ str(kvitamin[0]['unit']))
            for hozzavalok_db in hozzavalok:
               self.recept_out.append(hozzavalok_db['text'])
        return
    def mentes(self):
        with open(self.receptcime.text()+'.txt', 'w') as recept_text:
            recept_text.write(str(self.recept_out.toPlainText().encode('utf-8')))

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
