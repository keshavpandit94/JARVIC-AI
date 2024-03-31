# module for use this code
import os
import requests
import random
import pygame
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser

# Voice code
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)

#Speaking function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Starting time wise and intro for A.I
def wiseMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        print("Good Morning")
        speak("Good Morning")

    elif hour >= 12 and hour < 18:
        print("Good afternoon")
        speak("Good afternoon")
    else:
        print("Good evening")
        speak("Good evening")
    print("I am Rocket sir. Please tell me how may I help you")
    speak("I am Rocket sir. Please tell me how may I help you")

#Function for Listening and printing your A.I.
def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing..........")
        query = r.recognize_google(audio, language='en-in')
        print("User said: \n", query)

    except Exception as e:
        speak("Say that again please.......")
        print("Say that again please.......")
        return "None"
    return query.lower()

# Creat a function for live update weather in your current city.
def get_weather(api_key, city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error fetching data:", response.status_code)
        return None
 
def display_weather(data):
    if data:
        city = data['name']
        country = data['sys']['country']
        temperature = data['main']['temp']
        weather_desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        timestamp = data['dt']
        date_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        speak(f"Weather in {city}, {country} at {date_time}:")
        print(f"Weather in {city}, {country} at {date_time}:")
        speak(f"Temperature: {temperature}°C")
        print(f"Temperature: {temperature}°C")
        speak(f"Weather Description: {weather_desc}")
        print(f"Weather Description: {weather_desc}")
        speak(f"Humidity: {humidity}%")
        print(f"Humidity: {humidity}%")
        speak(f"Wind Speed: {wind_speed} m/s")
        print(f"Wind Speed: {wind_speed} m/s")
    else:
        print("No data available.")


#Function for play music random
def play_random_music(music_dir):
    # Initialize pygame
    pygame.init()
    # Set up the mixer to handle music
    pygame.mixer.init()
    # Get a list of all music files in the specified directory
    music_files = [os.path.join(music_dir, f) for f in os.listdir(music_dir) if f.endswith('.mp3')]
    if not music_files:
        print("No music files found in the specified directory.")
        return
    # Randomly select a music file to play
    random_music = random.choice(music_files)
    # Load and play the selected music file
    pygame.mixer.music.load(random_music)
    pygame.mixer.music.play()
    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    wiseMe()
    while True:
        query = takeCommand()
        # Logic for executing tasks based on query

        #Normal talk to A.I
        talks  = [['hello rocket', 'hello'], ['how are you', 'i am good and you'], ['i am good', 'good'], [
            'where are you from', 'your computer'], ['Sorry, I did not understand that.']]
        for talk in talks :
            if talk[0] in query :
                speak(talk[1])
                print(talk[1])
                break
        #open the your website.
        sites = [["youtube", "youtube.com"], ["google", "google.co.in"], ["github", "github.com"]]
        for site in sites:
            if f"open {site[0]}" in query:
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])  # Fix index to 1 instead of 2
                break

        #your question search for wekipedia or speak and print answer
        if "wikipedia" in query:
            print("Searching Wikipedia.....")
            speak("Searching Wikipedia.....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3) #your choces incess the sentence for 3 to 4,5,10.....etc
            speak("According to Wikipedia")
            print(results)
            speak(results)

        #Tell you time
        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            print(f"Time is {strTime}")

        #Tell you day and date
        elif "date" in query:
            current_datetime = datetime.datetime.now()
            # Format the date
            formatted_date = current_datetime.strftime("%d-%m-%Y")
            speak(f"Current Date:{formatted_date}")
            print(f"Current Date:{formatted_date}")
            # Get the day of the week
            day_of_week = current_datetime.strftime("%A")
            speak(f"Day of the Week:{day_of_week}")
            print(f"Day of the Week:{day_of_week}")

        #Open your news website
        elif "cricket news" in query:
            speak("open cricket news")
            print("Open Cricket News")
            webbrowser.open("https://www.jagran.com/cricket-hindi.html")

        #Play Music
        elif "play music" in query :
            # Specify the directory containing your music files
            music_directory = 'path/to/your/music/directory'
            play_random_music(music_directory)

        elif "today weather" in query:
            api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
            city_name = input("Enter city name: ")
            weather_data = get_weather(api_key, city_name)
            display_weather(weather_data)

        #you command to close your assisted
        elif "rocket close" in query:
            exit()
        #You command to reset your chat
        elif "reset chat" in query:
            chatStr = ""

        else:
            print("Chatting...")
            # chat(query)