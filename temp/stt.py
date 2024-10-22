import speech_recognition as sr
from threading import Thread
from queue import Queue
from pathlib import Path
from faster_whisper import WhisperModel
import logging
import keyboard
import pyaudio
import wave

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger("faster_whisper").setLevel(logging.WARNING)

messages = Queue()
recordings = Queue()
transcribed_texts = []

CHANNEL = 1
FRAME_RATE = 16000
RECORD_SECONDS = 5  # Increased for better recognition
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2
CHUNKS = 1024
INPUT_DEVICE = 1
VERBOSE = False

def record():
    p = pyaudio.PyAudio()
    stream = p.open(format=AUDIO_FORMAT,
                    channels=CHANNEL,
                    rate=FRAME_RATE,
                    input=True,
                    input_device_index=INPUT_DEVICE,
                    frames_per_buffer=CHUNKS)
   
    frames = []
   
    while messages.qsize() > 0:
        data = stream.read(CHUNKS)
        frames.append(data)
       
        if len(frames) == int(FRAME_RATE * RECORD_SECONDS / CHUNKS):
            recordings.put(b''.join(frames))
            frames = []
   
    stream.stop_stream()
    stream.close()
    p.terminate()

def load_model(model_size):
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    return model

def recognize(model: WhisperModel):
    while True:
        if not recordings.empty():
            audio_data = recordings.get()
            
            # Save the audio data to a temporary WAV file
            # Path("src/data").mkdir(parents=True, exist_ok=True)
            temp_wav_file = "temp.wav"
            with wave.open(temp_wav_file, "wb") as wf:
                wf.setnchannels(CHANNEL)
                wf.setsampwidth(SAMPLE_SIZE)
                wf.setframerate(FRAME_RATE)
                wf.writeframes(audio_data)
            
            # Use the audio file as the audio source
            segments, info = model.transcribe(temp_wav_file, beam_size=5)
            
            if VERBOSE:
                print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

            for segment in segments:
                transcribed_texts.append(segment.text)
                print(segment.text)
                
            # for segment in segments:
            #     # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))  # Read the entire audio file
            #     print(segment.text)
        
        if messages.qsize() == 0:
            break

def start_recording():    
    model_size = "small"
    model = load_model(model_size)
    logging.info(f"Whisper {model_size} Model loaded")

    # Start recording
    messages.put(True)
    logging.info("Recording started")

    record_thread = Thread(target=record)
    record_thread.start()
   
    transcribe_thread = Thread(target=recognize, args=(model,))
    transcribe_thread.start()
   
def stop_recording():
    messages.get()
    logging.info("Recording stopped")

def speech_to_text():
    start_recording()

    print("Press 'q' to stop recording")
    keyboard.wait('q')

    stop_recording()

    print("Transcribed texts:\n")
    print(transcribed_texts)
    return transcribed_texts
    
    
if __name__ == "__main__":

    # ### run wsisper (testing) ###########
    # whisper = WhisperModel("base", device="cuda", compute_type="float16")
    # transcribtions, info = whisper.transcribe('temp.wav', beam_size=5)
    # for segment in transcribtions:
    #     print(segment.text)
    ###################################



    ##### run script #########
    start_recording()
    
    print("Press 'q' to stop recording")
    keyboard.wait('q')
    
    stop_recording()
    
    print("Transcribed texts:\n")
    print(transcribed_texts)
    ###################################


    #### check mic devices ########
    # p = pyaudio.PyAudio()
    # for i in range(p.get_device_count()):
    #     print(i, p.get_device_info_by_index(i).get('name'))

    # p.terminate()