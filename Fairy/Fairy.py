import speech_recognition
import pyttsx3
import os
from datetime import date
from datetime import datetime

#Khởi tạo
Fairy_ear = speech_recognition.Recognizer() #nghe người dùng
Fairy_mouth = pyttsx3.init() #nói
Fairy_brain = "" #chưa có thông tin

while True:
    with speech_recognition.Microphone() as mic:
        print("\nFairy: Tôi đang nghe đây")
        audio = Fairy_ear.listen(mic, timeout = 5) #Fairy nghe bằng mic, tự tắt sau 5s (có thể điều chỉnh)
    print("\nFairy: ...")
    try:
        you = Fairy_ear.recognize_google(audio) #nghe và sẽ nói
    except:
        you = ""
    print("\nNgười dùng: " + you)

    if you == "":
        Fairy_brain = "Can you say again?"
    elif "hello" in you:
        Fairy_brain = "Hello Chí Vĩnh, what can I help you?"
    elif "hi" in you:
        Fairy_brain = "Hello Chí Vĩnh, what can I help you?"
    elif "today" in you: 
        today = date.today()
        Fairy_brain = today.strftime("%B %d, %Y")
    elif "date" in you:
        now = datetime.now()
        Fairy_brain = now.strftime("%H:%M:%S")
    elif "bye" in you:
        Fairy_brain = "Bye Chí Vĩnh"
        print("\nFairy: " + Fairy_brain)
        Fairy_mouth.say(Fairy_brain)
        Fairy_mouth.runAndWait()
        break
    else:
        Fairy_brain = "I was not built to understand it"

    print("\nFairy: " + Fairy_brain)
    Fairy_mouth.say(Fairy_brain)
    Fairy_mouth.runAndWait()