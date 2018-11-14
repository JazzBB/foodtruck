import requests
import json
import objectpath
from py_translator import Translator
from random import randint

APPID = ""
KULCS = ""
index_from = randint(1,4)
index_to = index_from - 1
if index_to < index_from:
    index_to = index_to + 2
response = requests.get("https://api.edamam.com/search?q=fish+lemon&app_id="+APPID+"&app_key="+KULCS+"&from="+str(index_from)+"&to="+str(index_to)+"&diet=low-carb&nutrients%5BCHOCDF%5D=45-50").json()

#Adatok kiszedése a JSONbol
response_tree = objectpath.Tree(response['hits'])
szenhidrat = tuple(response_tree.execute('$..CHOCDF'))
szemely = tuple(response_tree.execute('$..yield'))
recept_neve = tuple(response_tree.execute('$..label'))
hozzavalok = tuple(response_tree.execute('$..ingredients'))
fozesi_ido = tuple(response_tree.execute('$..totalTime'))
kaloria = tuple(response_tree.execute('$..ENERC_KCAL'))
#print, aztan majd megy GUIra

print(Translator().translate(text=recept_neve[0],dest='hu').text)
print(szemely[0])
print("Össz szénhidrát tartalom:"+ str(szenhidrat[0]['quantity'])+ str(szenhidrat[0]['unit']))
egy_adag_ch = int(szenhidrat[0]['quantity'])/int(szemely[0])
print("Egy adag szénhidrát tartalma: "+str(egy_adag_ch))
print("Össz kalória tartalom: "+str(kaloria[0]['quantity'])+ str(kaloria[0]['unit']))
print("Főzési idő: "+str(fozesi_ido[0]))
print("Hozzávalók\n----------------------------------------------------------------")
for hozzavalok_db in hozzavalok:
    print(Translator().translate(text=hozzavalok_db['text'],dest='hu').text)
