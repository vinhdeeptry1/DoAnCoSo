import googletrans
from googletrans import Translator
# print(googletrans.LANGUAGES)
t = Translator(service_urls=[
       'translate.google.com',
     'translate.google.co.kr',
     ])

while True:
    dich = input ("Nhập từ cần dịch: ")
    candich = t.translate (dich, src= "en", dest= "vi")
    print("Fairy: " + candich.text)
    if dich == "Exit":
        candich = t.translate (dich, src= "en", dest= "vi")
        print("Fairy: " + candich.text)
        break