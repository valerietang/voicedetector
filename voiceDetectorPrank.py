import os
import vosk
import pygame
import threading
import pyaudio
import json  

pygame.mixer.init()

is_playing = False

def play_sound(sound_file):
    global is_playing
    is_playing = True
    pygame.mixer.music.load(sound_file)  
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    is_playing = False

def listen_for_name(target_names, sound_files):
    global is_playing

    model_path = r"C:\Users\Valerie\Downloads\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15"
    if not os.path.exists(model_path):
        print("Model not found.")
        return

    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    microphone = pyaudio.PyAudio()
    stream = microphone.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print(f"Listening for {target_names}... (Type 'stop' to stop)")

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            spoken_text = result_dict.get('text', '')

            for i, name in enumerate(target_names):
                if name.lower() in spoken_text.lower():
                    print(f"'{name}' detected!")
                    if not is_playing:
                        sound_file = sound_files[i]
                        threading.Thread(target=play_sound, args=(sound_file,)).start()
                    break

def user_input():
    global is_playing
    while True:
        command = input()  
        if command.lower() == "stop":
            if is_playing:
                print("Sound Stopped")
                pygame.mixer.music.stop()  
                is_playing = False
            else:
                print("There is nothing to stop.")

target_names = ["funny", "car", "crazy", "going", "busy"]  
sound_files = [
    r"C:\changethistoyourownfile.mp3",    
    r"C:\changethistoyourownfile.mp3",
    r"C:\changethistoyourownfile.mp3",
    r"C:\changethistoyourownfile.mp3",
    r"C:\changethistoyourownfile.mp3"   
]

listener_thread = threading.Thread(target=listen_for_name, args=(target_names, sound_files))
listener_thread.start()

user_input()
