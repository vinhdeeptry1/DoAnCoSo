import googletrans
from googletrans import Translator
# print(googletrans.LANGUAGES)
t = Translator(service_urls=[
       'translate.google.com',
     'translate.google.co.kr',
     ])

while True:
    dich = input ("Translate: ")
    candich = t.translate (dich, src= "vi", dest= "en")
    print("Fairy: " + candich.text)
    if dich == "Thoát":
        candich = t.translate (dich, src= "vi", dest= "en")
        print("Fairy: " + candich.text)
        break