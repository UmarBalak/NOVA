import webbrowser
import wikipedia
import pyttsx3
import os
from Api import api_key
import openai
from tm import strTime
import datetime
import time
from googletrans import  Translator
import speech_recognition as sr
from keyboard import press_and_release
from keyboard import press
openai.api_key = "Your OPENAI API key"
completion = openai.Completion()
strTime = datetime.datetime.now().strftime("%H:%M:%S")

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voices",voices[1].id) 
engine.setProperty('rate',180)




def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    print(audio)


def translation(Text):  
    line = str(Text)
    trans = Translator()
    res = trans.translate(line)
    data = res.text
    return data


def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listning...')
        r.pause_threshold = 1
        audio = r.listen(source)

    
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio,language='en')
        
    except Exception as e:
        return "None"
    return query


def replyBrain(query,ans = None):
    training = open("chatlog.txt","r")
    training_template = training.read()
    training.close()

    if ans is None:
        ans = training_template
        prompt = f'{ans}Me : {query}\nJarvis : '
        response = completion.create(
        model = "text-davinci-002",
        prompt = prompt,
        temperature = 0.5,
        max_tokens = 500,
        top_p = 0.3,
        frequency_penalty = 0.5,
        presence_penalty = 2)
                        
    answer = response.choices[0].text.strip()
    answer = answer.lower()


    if query in training_template:
        training_template_update = training_template
    else:
        training_template_update = training_template + f'\nMe : {query} \nJarvis : {answer}'
    training = open("chatlog.txt","w")
    training.write(training_template_update)
    training.close()
    if answer == "i'm sorry, i don't understand what you're trying to say. can you please rephrase your question?":
        return None
    else:
        speak(answer)
        

    if 'opening youtube' in answer:
        webbrowser.open('https://youtube.com/')

    elif 'searching' in answer:
        if 'youtube' in answer:
            answer = answer.replace('searching',"").replace('for',"").replace('on',"").replace('youtube',"").replace('...',"").replace('"',"").replace('"',"")
            print(answer)
            webbrowser.open('https://www.youtube.com/results?search_query=' +answer)

        elif 'wikipedia' in answer:
            answer = answer.replace('searching',"").replace('for',"").replace('wikipedia',"").replace('on',"")
            result = wikipedia.summary(answer, sentences = 3)
            speak(result)

        elif 'google' in answer:
            answer = answer.replace('searching',"").replace('for',"").replace('google',"").replace('on',"").replace('...',"")
            print(answer)
            webbrowser.open('https://www.google.com/results?search_query=' +answer)
        elif 'chrome' in answer:
            answer = answer.replace('searching',"").replace('for',"").replace('chrome',"").replace('on',"").replace('...',"")

    elif 'closing youtube' in answer:
        os.system('TASKKILL /F youtube.com')
    elif 'opening colab' in answer:
        webbrowser.open('https://colab.research.google.com/')

    elif 'opening google' in answer:
        webbrowser.open_new_tab('https://www.google.com/')

    elif 'opening chrome' in answer:
        webbrowser.open_new_tab('"C:\Program Files\Google\Chrome\Application\chrome.exe"')

    elif 'new tab' in answer:
        press_and_release('ctrl + t')

    elif 'closing the current tab' in answer:
        press_and_release('ctrl + w')

    elif 'turning on bluetooth' in answer:
        press_and_release('win + a')
        time.sleep(2)
        press('right arrow')
        time.sleep(3)
        press('enter')
        time.sleep(2)

    elif 'turning off bluetooth' in answer:
        press_and_release('win + a')
        press_and_release('end')
        press_and_release('enter')
    elif 'minimizing' in answer:
        press_and_release('win + down arrow')
        time.sleep(0.00001)
        press_and_release('win + down arrow')
    elif 'new window' in answer:
        press_and_release('ctrl + n')
            
    elif 'closing the current window' in answer or 'closing the window' in answer:
        press_and_release('alt + F4')

    elif 'history' in answer:
        press_and_release('ctrl + h')

    elif 'download' in answer:
        press_and_release('ctrl + j')

    elif 'closing the active document' in answer:
        press_and_release('ctrl + F4')


    elif 'bookmark' in answer:
        press_and_release('ctrl + d')   
        press('enter')

    elif 'incognito' in answer:
        press_and_release('Ctrl + Shift + n')

    elif 'switch tab' in answer:
        tab = answer.replace("switch tab ", "")
        Tab = tab.replace("to","")
        num = Tab
        bb = f'ctrl + {num}'
        press_and_release(bb)
while True:
    query = listen().lower()
    replyBrain(query)
