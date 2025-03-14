from elevenlabs import stream, play
from elevenlabs.client import ElevenLabs
import openai
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import threading
from pynput import keyboard
import dotenv
import os

dotenv.load_dotenv()

from utils import record_audio
from chat_res import get_chat_response
from tts import get_audio_response

elevenlabs_api = os.getenv("ELEVENLABS_API")
groq_api = os.getenv("GROQ_API")

sample_rate = 16000

openai_client = openai.Client(
    api_key=os.getenv("OPENAI_API")
)

groq_client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api
)




def get_transcription(file_path: str, model: str = "whisper-large-v3-turbo"):
    g_stt = groq_client.audio.transcriptions.create(
        model=model,
        file=open(file_path, "rb"),
        language="en"
    )
    return g_stt.to_dict()['text']



def start_assistant():

    global recording, is_recording
    is_recording = False
    recording = record_audio()
    transcription = get_transcription('record.wav')
    print(f"Transcription: {transcription}")
    chat_response = get_chat_response(transcription)
    print(f"Chat response: {chat_response}")
    audio_response = get_audio_response(chat_response,
                                        play_audio=True,
                                        use_melotts=True)
    return

if __name__ == '__main__':
    chatting = True
    def on_press_q(key):
        global chatting
        if str(key) == "'q'":
            chatting = False
            print("Exiting...")
            os._exit(69)
            return False
            
    listener = keyboard.Listener(on_press=on_press_q)
    listener.start()
    
    while chatting:
        start_assistant()
    if listener.is_alive():
        listener.stop()