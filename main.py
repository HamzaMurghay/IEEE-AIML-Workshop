import os.path
import requests

import speech_recognition as sr
from speech_recognition import UnknownValueError, WaitTimeoutError

import pyttsx3

import webbrowser as wb
import subprocess as sp

import google.generativeai as genai

genai.configure(api_key='your_api_key')
model = genai.GenerativeModel('gemini-1.5-flash')

weather_api = "your_api_key"
weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?appid={weather_api}&q=Mumbai"


def give_ai_response(user_query):
    if user_query:
        response = model.generate_content(user_query)

        if not os.path.exists("Gemini Prompts"):
            os.mkdir("Gemini Prompts")

        with open(f"Gemini Prompts/{user_query}.md", "w") as file:
            file.write(response.text)

        print("Done Sir!")
        say("Done Sir!")


def terminate():
    print("\nTerminating Execution, See you next time sir!")
    say("Terminating Execution, See you next time sir!")
    exit()


def take_voice_command():

    try:
        r = sr.Recognizer()
        with sr.Microphone() as mic:
            r.adjust_for_ambient_noise(mic, duration=0.3)
            audio = r.listen(mic, timeout=20)
            user_query = r.recognize_google(audio, language="en-US")
            print(f"You said: {user_query}\n")
            return user_query

    except UnknownValueError:
       return "Error! Please repeat what you said"
    except WaitTimeoutError:
        terminate()


def say(text):
    voice_engine = pyttsx3.init()
    voice_engine.say(text)
    voice_engine.runAndWait()

print("Hello sir, I am Jarvis, The Artificial Intelligence designed to assist you.\n")
say("Hello sir, I am Jarvis, The Artificial Intelligence designed to assist you.")


sites = [["Youtube","www.youtube.com"],["Google", "www.google.com"],["Instagram", "www.instagram.com"],
         ["Spotify", "open.spotify.com"]]

apps = [["Notepad","notepad.exe"],["Calculator", "calc.exe"],
        ["Chrome", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]]

while True:
    print("Listening for query....")
    query = take_voice_command()
    say(query)

    for site in sites:
        if f"open {site[0].lower()}" in query.lower():
            print(f"Opening {site[0]} Sir...")
            say(f"Opening {site[0]} Sir...")
            wb.open(f"https://{site[1]}")  # opening sites

    for app in apps:
        if f"open {app[0].lower()}" in query.lower():
            print(f"Opening {app[0]} Sir...")
            say(f"Opening {app[0]} Sir...")
            sp.call([app[1]])  # opening applications

    if "using gemini" in query.lower():
        give_ai_response(query.lower().split("using gemini")[0].strip())

    if "weather" in query.lower():
        weather_response = requests.get(weather_api_url).json()
        print("Weather Description is:", weather_response['weather'][0]['main'])

    if "terminate" in query.lower() or "exit" in query.lower():
        terminate()
