import os
import pygame
import time
from dj_cara import cara_tts
import eventlet
import requests
# generate audio from text
# text_prompt = """
#      Hey, hey, hey! You're hanging out with DJ Jazzy and we’re about to get our groove on with the ‘All out 80s’ playlist! Ah, the 80s – when the hair was big, the fashion was loud, and the music was larger than life. Get ready to ride the retro wave with some of the decade’s biggest hits. And speaking of big hits, let’s kick things off with a track that absolutely screams 80s! Stay tuned and don't go anywhere, because the beats are just getting started right here with your favorite, DJ Jazzy! 📻🎶
# """
def speak(file):
    # tts = gTTS(text=text, lang='en')
    # tts.save("response.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        eventlet.sleep(0.1) 

    pygame.mixer.quit()
    eventlet.sleep(0.5)
    
    os.remove(file)

