import pygame
from gtts import gTTS
import os
import time

pygame.mixer.init()

voice_enabled = True


def set_voice(state):
    global voice_enabled
    voice_enabled = state


def speak(text):

    if not voice_enabled:
        return

    filename = "temp_voice.mp3"

    try:
        tts = gTTS(text=text, lang="en")
        tts.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.2)

        pygame.mixer.music.unload()

    finally:
        if os.path.exists(filename):
            os.remove(filename)


def stop_voice():
    """Stop voice playback immediately"""
    pygame.mixer.music.stop()