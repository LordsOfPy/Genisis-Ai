import datetime
import pyttsx3
import speech_recognition as sr
import pyaudio
import time
import os
import webbrowser
import wikipedia
import pywhatkit
import pyautogui
import pyjokes
import subprocess as sp
import cv2
import mediapipe as mp
from PIL import Image,ImageEnhance,ImageFilter
import qrcode
from ecapture import ecapture as ec
from playsound import playsound
import requests
import pvporcupine
import sys


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate',200)
cap = cv2.VideoCapture(1)
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)
API_KEY = open('API_KEY').read()
SEARCH_KEY = open('SEARCH_ENG_ID').read()

def send_whatsapp_message(number, message):
    pywhatkit.sendwhatmsg_instantly(f"+971{number}", message)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Wait For A Moment")
        query = r.recognize_google(audio, language='en-in',pfilter=0)
        print(f"You Just Said: {query}\n")
    except Exception as e:
        print(e)
        speak("Please Tell Me Again")
        query = "none"
    return query


def wishing():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning")
        speak("Good Morning")
    elif hour >= 12 and hour < 17:
        print("Good Afternoon")
        speak("Good Afternoon")
    else:
        print("Good Evening Sir")
        speak("Good Evening Sir")

if __name__ == "__main__":
    wishing()
    while True:
        query = commands().lower()
        if 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir, the time is {strTime}")

        elif 'open google' in query:
            speak("Opening Google sir...")
            os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk")

        elif 'wikipedia' in query:
            speak("Searching In WikiPedia")
            try:
                query = query.replace('wikipedia', '')
                results = wikipedia.summary(query, sentences=5)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except:
                speak("No Result Found")
                print("No Result Found")

        elif 'play' in query:
            try:
                query = query.replace('play', '')
                speak('Playing' + query)
                pywhatkit.playonyt(query)
            except:
                speak("No Result Found")

        elif 'type' in query:
            query = query.replace('type', '')
            speak("Writing")
            pyautogui.write(query)

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif 'exit' in query:
            speak('I am Leaving')
            print('I am Leaving')
            quit()

        elif 'close' in query:
            pyautogui.hotkey('alt', 'F4')
            speak("Closing Window")

        elif 'minimize' in query or 'minimise' in query:
            speak('Minimizing')
            pyautogui.hotkey('win', 'down')

        elif 'maximize' in query or 'maximise' in query:
            speak('Maximizing')
            pyautogui.hotkey('win', 'up')

        elif 'screenshot' in query:
            speak('Taking ScreenShot')
            pyautogui.press('prtsc')

        elif 'search' in query:
            search = query.replace('search', '')
            speak('searching')
            try:
                resInfo = pywhatkit.info(search)
                resInfo = resInfo[len(resInfo)-1]
                print(resInfo)
                speak(resInfo)
            except:
                print("Error")

        elif 'thank you' in query:
            speak("That,s My Pleasure")
            print("That,s My Pleasure")

        elif 'how are you' in query:
            speak("Fine ")
            print("Fine ")

        elif 'send whatsapp message' in query:
            speak("What is the Number of reciver")
            number = input("What is The Number: ")
            speak("What Should I Send")
            message = input("What Should I Message: ")
            send_whatsapp_message(number, message)
            speak("sending whatsapp message")

        elif 'open command prom' in query:
            speak("opening command")
            os.system('start cmd')

        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open('youtube.com')

        elif 'face mesh' in query or 'face mess' in query or 'face wash' in query or 'face mask' in query or 'fish mesh' in query :
            while True:
                success, img = cap.read()
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = faceMesh.process(imgRGB)
                if results.multi_face_landmarks:
                    for faceLms in results.multi_face_landmarks:
                        mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec)

                cv2.imshow("Image", img)
                if cv2.waitKey(33) == ord('a'):
                    cv2.destroyAllWindows()
                    break

        elif 'shutdown' in query:
            pywhatkit.shutdown(50)
            speak("shut down in 50 sec")
            query = commands().lower()
            while True:
                if 'cancel' in query:
                    pywhatkit.cancel_shutdown()
                    break

        elif 'enchant image' in query or 'ancient image' in query:
            print("#No Quotes Symbol")
            imgenr = input("File Path: ")
            try:
                imgc = Image.open(imgenr)
                print("Options: Sharpness,Brightness,Color,Contrast")
                query = commands().lower()
                enc = input("Enter Increase Rate: ")
                while True:
                    if 'sharpness' in query:
                        enc_img = ImageEnhance.Sharpness(imgc)
                        enc_img.enhance(enc)
                        break
                    if 'brightness' in query:
                        enc_img = ImageEnhance.Brightness(imgc)
                        enc_img.enhance(enc)
                        break
                    elif 'colour' in query:
                        enc_img = ImageEnhance.Color(imgc)
                        enc_img.enhance(enc)
                        break
                    elif 'contrast' in query:
                        enc_img = ImageEnhance.Contrast(imgc)
                        enc_img.enhance(enc)
                        break
                    else:
                        query = commands().lower()
            except:
                print("Error Generating Image")

        elif 'cancel shutdown' in query:
            pywhatkit.cancel_shutdown()

        elif 'qr code' in query:
            def gen_qr_code(text, filename):
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(text)
                qr.make(fit=True)
                img = qr.make_image(fill_color="#6aff9b", back_color="black")
                img.save(filename)
                img.show()

            text = input("Website: ")

            filename = "qr_code.png"

            gen_qr_code(text, filename)
            print(f"Qr Code Saved As {filename}")
            speak("Qr Code Generated")

        elif 'take a photo' in query:
            speak("Cheeeeeesss")
            ec.capture(1,"camera","img.jpg")

        elif "alarm" in query:
            speak("Enter What Hour to set")
            alaramHour = int(input("Enter Hour: "))

            speak("Enter What Minute in that hour to set")
            alaramMin = int(input("Enter Minute: "))

            speak("Enter Am or Pm")
            alaramAm = input("Enter Am / Pm : ")

            if alaramAm=="Pm" or alaramAm=="pm" or alaramAm=="PM":
                alaramHour+=12

            while True:
                if alaramHour== datetime.datetime.now().hour and alaramMin==datetime.datetime.now().minute:
                    print("Playing...")
                    playsound("mixkit-classic-alarm-995.wav")
                    break

        elif "image" in query:
            speak("Tell Me What Image To Get")
            search_query = input("Image: ")
            url = 'https://www.googleapis.com/customsearch/v1'
            params = {
                'q': search_query,
                'key': API_KEY,
                'cx': SEARCH_KEY,
                'searchType':'Image'
            }
            response = requests.get(url, params=params)
            resuls = response.json()

            if 'items' in resuls:
                webbrowser.open(resuls['items'][1]['link'])
        
        elif "hello" in query or "hi" in query:
            wishing()
        
        elif "what is your name" in query or "what's your name" in query:
            speak("My Name Is Gensise")