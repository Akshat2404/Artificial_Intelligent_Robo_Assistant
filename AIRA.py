# AIRA[Artificial Intelligence Robot Assistant] using Python 3.9
# YouTube Video Link - Code With Harry
# https://www.youtube.com/watch?v=Lp9Ftuq2sVI&list=RDCMUCeVMnSShP_Iviwkknt83cww&start_radio=1&rv=Lp9Ftuq2sVI&t=12

import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import time
import ssl
import smtplib
import pywhatkit
import pyjokes
import pyautogui as pg

def speak(audio):
    """It speaks the sentence passed as an 'audio' argument."""
    print(f'AIRA: {audio}')
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    """Takes a micrphone audio-input command from the user and returns string output."""
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        # r.energy_threshold = 500
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in', )
        # print(f'{USER} says: {query}')

    except Exception as e:
        # print(e)
        print('Apologies! Could you please Repeat...')
        # speak('Apologies! Could you please Repeat...')
        return 'None'
    
    return query

def wishMe():
    """It greets the user as per the time when used and for assistance."""
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak('Good Morning!!!')
    elif hour>=12 and hour<18:
        speak('Good Afternoon!!!')
    else:
        speak('Good Evening!!!')
    speak('Master, how can I address you?')
    global USER
    USER = takeCommand()
    speak(f'Hello {USER}, I am AIRA. How may I help you?')

def sendEmail(to, content):
    """It helps to send an email with the content user speaks."""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    f=open('Pass.txt', 'r')
    pwd = f.read()
    f.close()
    context = ssl.create_default_context()
    sender_email='19bce246@nirmauni.ac.in'
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender_email, pwd)
    server.sendmail(sender_email, to, content)
    server.close()

def sendWhatsApp(contact_number, msg):
    hrs = int(datetime.datetime.now().hour)
    mins = int(datetime.datetime.now().minute)+1
    pywhatkit.sendwhatmsg(contact_number, msg, hrs, mins)
    # pg.press('Enter')

if __name__ == '__main__':
    USER = 'Master' # Akshat
    # Speech API from MicroSoft
    engine = pyttsx3.init('sapi5') # SAPI -> Microsoft Speech API Version 5
    voices = engine.getProperty('voices')
    print(voices[2].id)
    engine.setProperty('voice', voices[2].id)
    
    wishMe()
    previousCommand = 'Akshat'
    while True:
        query = takeCommand()
        print(f'{USER}: {query}')
        query=query.lower()
        if query == 'same' or query == 'repeat':
            query = previousCommand
            print(f'{USER}: {query}')
        else:
            previousCommand = query

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=10)
            speak('According to Wikipedia, ')
            # print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open('youtube.com')

        elif 'open google' in query:
            webbrowser.open('google.com')

        elif 'open stackoverflow' in query:
            webbrowser.open('stackoverflow.com')

        elif 'play music' in query or 'play song' in query:
            music_dir = "D://CSE//Python//Songs//"
            songs = os.listdir(music_dir)
            print(songs)
            x = random.randint(0, len(songs))
            os.startfile(os.path.join(music_dir, songs[x]))
            song_name = music_dir + songs[x]
        
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f'{USER}, the time is: {strTime}')

        elif 'open code' in query or 'visual studio' in query:
            code_path = "C://Users//Akshat//AppData//Local//Programs//Microsoft VS Code//Code.exe"
            os.startfile(code_path)

        elif 'mail' in query:
            try:
                speak('Please enter the mail-ID you want to send...')
                to = input('Whom do you want to send this mail?: ')
                speak('What should I say?')
                content = takeCommand()
                sendEmail(to, content)
                speak('E-Mail sent Succesfully!!')
            except Exception as e:
                print(e)
                speak(f"Sorry {USER}, couldn't send the E-Mail")

        elif 'whatsapp' in query:
            speak('Please enter the contact number to which whatsApp message is to be sent: ')
            num = input('Contact Number: ')
            contact_number = '+91' + num
            speak('Please speak the message you want to send:- ')
            msg = takeCommand()
            if contact_number[1:].isnumeric() and len(contact_number)==13:
                sendWhatsApp(contact_number, msg)
                speak('Message sent successfully!!')
            else:
                speak('Incorrect information. Failed to send the message...')

        elif 'joke' in query:
            speak(pyjokes.get_joke())
        
        elif 'quit' in query or 'bye' in query or 'close' in query or 'exit' in query or 'end' in query:
            speak('AIRA signing off!!')
            break

        elif 'sleep' in query:
            time.sleep(60)
            speak(f"Hello {USER}, I'm back. How can I help?")

        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")

        else:
            speak(f"Sorry {USER}, couldn't understand your command...")
            speak('Please try again...')
