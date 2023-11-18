import os
import webbrowser
import smtplib
import pyttsx3
import geocoder
import tweepy
from bs4 import BeautifulSoup
import requests
import pywhatkit as kit
import time
import pyautogui
import speech_recognition as sr
import wikipediaapi
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client
from playsound import playsound
import pygame
import tweepy
from geopy.geocoders import Nominatim
import folium

def notepad():
    os.system("notepad.exe")

def open_chrome():
    webbrowser.open("http://www.google.com", new=2)


def send_email():
    recipient = input("Recipient email:")
    subject = input("Subject:")
    body = input("Body:")
    
    smtp_server = 'smtp.gmail.com'     
    smtp_port = 587                     
    sender_email = 'sendermail@gmail.com'
    sender_password = 'password_here'
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        print("Mail sent!")
        
    except Exception as e:
        print(f"Error sending message: {str(e)}")
    

def send_message(opt):
    recipient = input("Recipient (with country code): ")
    message = input("Message:")
    
    if opt=="whats":
        
        try:
            kit.sendwhatmsg_instantly(recipient, message)
            time.sleep(20)
            pyautogui.press("enter")
            print("Message Sent!")
        except Exception as e:
            print(f"Error sending message: {str(e)}")
    elif opt=="sms":
        
        account_sid = 'account_sid'
        auth_token = 'account_token'
        twilio_phone_number = 'twilio_phone_number'

        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_=twilio_phone_number,
                body=message,
                to=recipient
            )
            print("Message sent!")
        except Exception as e:
            print(f"Error sending message: {str(e)}")


def chat_with_gpt():
    url = "https://chat.openai.com/"
    webbrowser.open(url)

def get_geolocation():
    # Get the current location based on GPS coordinates
    current_location = geocoder.ip('me')

    if current_location:
        latitude, longitude = current_location.latlng
        location_name = current_location.address if current_location.address else f"{latitude}, {longitude}"
        print(f"Current Location: {location_name}, Latitude: {latitude}, Longitude: {longitude}")

        # Create a map centered around the current coordinates
        map_location = folium.Map(location=[latitude, longitude], zoom_start=10)

        # Add a marker for the current location
        folium.Marker([latitude, longitude], tooltip=location_name).add_to(map_location)

        # Display the map
        map_location.save("current_location_map.html")
    else:
        print("Unable to determine current location.")
    
    

def get_twitter_trending(woe_id=1):
    consumer_key = 'CONSUMER_KEY'
    consumer_secret = 'CONSUMER_SECRET'
    access_token = 'ACCESS_TOKEN'
    access_token_secret = 'ACCESS_TOKEN_SECRET'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:

        trends = api.trends_place(id=woe_id)
        trending_topics = trends[0]['trends']

        print("Current trending topics:")
        for index, topic in enumerate(trending_topics, start=1):
            print(f"{index}. {topic['name']}")

    except tweepy.TweepError as e:
        print(f"Error: {e}")

def get_hashtag_posts(count=10):
    consumer_key = 'YOUR_CONSUMER_KEY'
    consumer_secret = 'YOUR_CONSUMER_SECRET'
    access_token = 'YOUR_ACCESS_TOKEN'
    access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    hashtag = input("Hashtag to search: ")
    try:
        tweets = tweepy.Cursor(api.search, q=f"#{hashtag}", lang="en").items(count)

        print(f"Top {count} posts for #{hashtag}:\n")
        for index, tweet in enumerate(tweets, start=1):
            print(f"{index}. {tweet.text}\n")

    except tweepy.TweepError as e:
        print(f"Error: {e}")

def get_wikipedia_data(lang='en'):
    wiki_wiki = wikipediaapi.Wikipedia('en') 
    topic = input("Topic to search: ") # Topic You Want to Fetch

    page = wiki_wiki.page(topic)
    if page.exists():
        print("Title:", page.title)
        print("Content:")
        print(page.text)
    else:
        print(f"The page '{topic}' does not exist on Wikipedia.")

def play_audio():
    file_path = "path/to/your/audio/file.mp3"
    try:
        playsound(file_path)
    except Exception as e:
        print(f"Error: {e}")

def play_video():
    file_path = "path/to/your/video/file.mp4"
    pygame.init()

    try:
        # Initialize Pygame
        pygame.init()

        # Set the window size based on the video resolution
        video_info = pygame.display.Info()
        screen = pygame.display.set_mode((video_info.current_w, video_info.current_h), pygame.FULLSCREEN)
        
        # Load the video
        pygame.mixer.quit()
        pygame.display.set_caption("Video Player")
        pygame.mouse.set_visible(False)

        # Create a Video object
        video = pygame.movie.Movie(file_path)
        video_screen = pygame.Surface(video.get_size()).convert()

        video.set_display(video_screen)
        video.play()

        clock = pygame.time.Clock()

        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False

            screen.blit(video_screen, (0, 0))
            pygame.display.flip()
            clock.tick(60)

            if not video.get_busy():
                playing = False

    except Exception as e:
        print(f"Error: {e}")

    pygame.quit()

def speak_text():
    text = input("Enter the text to speak: ")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error with the request to Google API; {0}".format(e))
        
def adjust_volume(text):
    if "increase volume" in text:
        pyautogui.press("volumeup")
        print("Volume increased")
    elif "decrease volume" in text:
        pyautogui.press("volumedown")
        print("Volume decreased")

def control_volume():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            adjust_volume(text)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")


while True:
    print("\n**** Menu ****")
    print("1. Notepad")
    print("2. Chrome")
    print("3. WhatsApp")
    print("4. Email")
    print("5. SMS")
    print("6. ChatGPT")
    print("7. Geolocation")
    print("8. Twitter Trending")
    print("9. Hashtag Posts")
    print("10. Wikipedia Search")
    print("11. Audio Player")
    print("12. Video Player")
    print("13. Text-to-Speech")
    print("14. Speech-to-Text")
    print("15. Control volume")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        notepad()
    elif choice == '2':
        open_chrome()
    elif choice == '3':
        send_message("whats")
    elif choice == '4':
        send_email()
    elif choice == '5':
        send_message("sms")
    elif choice == '6':
        chat_with_gpt()
    elif choice == '7':
        get_geolocation()
    elif choice == '8':
        get_twitter_trending()
    elif choice == '9':
        get_hashtag_posts()
    elif choice == '10':
        get_wikipedia_data()
    elif choice == '11':
        play_audio()
    elif choice == '12':
        play_video()
    elif choice == '13':
        speak_text()
    elif choice == '14':
        speech_to_text()
    elif choice == '15':
        control_volume()
  
    elif choice == '0':
        break
    else:
        print("Invalid choice. Please try again.")
