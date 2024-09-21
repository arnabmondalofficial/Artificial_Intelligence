import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import webbrowser
import wikipedia
import openai
import os
import requests

# Replace with your actual OpenWeatherMap API key
API_KEY = '9c17c19df8585b055938e95fb917fc94'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"


# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty("rate", 128)

# Set up OpenAI API key
openai.api_key = os.getenv('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')  # Ensure this environment variable is set


def talk(text):
    engine.say(text)
    engine.runAndWait()


def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Choose the desired model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        return "I'm sorry, I couldn't process that request at the moment."

def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listener.pause_threshold = 1
        voice = listener.listen(source)
        try:
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'comet' in command:
                command = command.replace('comet', '')
                print(f"Command received: {command}")
                return command
            else:
                # If 'comet' is not mentioned, treat it as an AI query
                print(f"AI Query received: {command}")
                return command
        except Exception as e:
            print(f"Error: {e}")
            return "Sorry, I did not catch that."



def run_comet():
    # Initial greeting
    talk('I am awake Sir')
    talk('What do you want me to do for you?')

    while True:
        command = take_command()

        if not command:
            continue  # Skip if command is empty

        # Predefined Commands
        if 'introduce yourself' in command:
            talk('I am Jarvis, a virtual assistant created, inspired by the AI Jarvis from Iron Man')

        elif 'hi' in command:
            talk('Hello Sir')

        elif 'hello' in command:
            talk('Hello Sir')

        elif 'how are you' in command:
            talk('I am fine Sir, What about you')

        elif 'play' in command:
            song = command.replace('play', '')
            talk('Playing ' + song)
            pywhatkit.playonyt(song)

        elif 'time' in command:
            time_now = datetime.datetime.now().strftime('%I:%M %p')
            print(time_now)
            talk("Current time is " + time_now)

        elif 'date' in command:
            current_date = datetime.datetime.now().strftime('%d/%m/%y')
            print(current_date)
            talk("Current date is " + current_date)

        elif 'thank you' in command:
            talk('Welcome Sir')
            talk('What more do I need to do for you')

        elif 'open google' in command:
            talk('Opening Google')
            webbrowser.open('https://www.google.com')

        elif 'open mail' in command:
            talk('Opening mail')
            webbrowser.open("https://www.mail.google.com")

        elif 'open youtube' in command:
            talk('Opening YouTube')
            webbrowser.open('https://www.youtube.com')

        elif 'open facebook' in command:
            talk('Opening Facebook')
            webbrowser.open('https://www.facebook.com/')

        elif 'open instagram' in command:
            talk('Opening Instagram')
            webbrowser.open('https://www.instagram.com/')

        elif 'open twitter' in command:
            talk('Opening Twitter')
            webbrowser.open('https://www.twitter.com/')

        elif 'open discord' in command:
            talk('Opening Discord')
            webbrowser.open('https://discord.com/')

        elif 'netflix' in command:
            talk('Opening Netflix')
            webbrowser.open('https://www.netflix.com/')

        elif 'amazon prime' in command:
            talk('Opening Amazon Prime')
            webbrowser.open('https://www.primevideo.com/')

        elif 'open hotstar' in command:
            talk('Opening Hotstar')
            webbrowser.open('https://www.hotstar.com/')

        elif 'open wikipedia' in command:
            talk('Opening Wikipedia')
            webbrowser.open('https://www.wikipedia.com')

        elif 'search' in command:
            talk('Searching')
            query = command.replace('search', '')
            try:
                info = wikipedia.summary(query, sentences=2)
                print(info)
                talk(info)
            except wikipedia.exceptions.DisambiguationError as e:
                talk("There are multiple results for that query. Please be more specific.")
            except wikipedia.exceptions.PageError:
                talk("I couldn't find any information on that topic.")

        elif 'who' in command or 'what' in command:
            talk('Finding')
            try:
                info = wikipedia.summary(command, sentences=3)
                print(info)
                talk(info)
            except wikipedia.exceptions.DisambiguationError as e:
                talk("There are multiple results for that query. Please be more specific.")
            except wikipedia.exceptions.PageError:
                talk("I couldn't find any information on that topic.")

        elif 'i love you' in command:
            talk('I am sorry. Being digital I do not have emotions or feelings, but my master does.')

        elif 'good morning' in command:
            talk('Good Morning Sir. Wish you have a great day ahead')

        elif 'good afternoon' in command:
            talk('Good Afternoon Sir')

        elif 'good night' in command:
            talk('Good Night Sir. Wish to help you tomorrow!')
            break

        elif 'i hate you' in command:
            talk(
                'I am sorry for the trouble. Give me a chance to prove myself and please do not blame my master for any of my mistakes.')

        elif 'weather' in command:
            curr_wea = get_weather(city_name)
            talk(curr_wea)

        elif 'exit' in command:
            talk("I am about to go offline. If you need me, just click the run button! Thank you!")
            break

        else:
            # AI-Driven Response
            print("Sending query to OpenAI...")
            response = ask_openai(command)
            print(f"AI Response: {response}")
            talk(response)

if __name__ == "__main__":
    run_comet()
