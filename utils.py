from pynput import keyboard
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import threading
import sys

def record_audio(sample_rate=16000):
    global recording, is_recording
    is_recording = True  
    recording = None
    frames = []
    
    def on_press(key):
        global is_recording
        try:
            if str(key) == "'x'":
                print("\nStopping recording...")
                is_recording = False
                return False  
                
        except (AttributeError, TypeError):
            pass 
    
    def start_recording():
        global recording, is_recording
        
        print("Recording... Press X to stop.")
        stream = sd.InputStream(samplerate=sample_rate, channels=1)
        stream.start()
        
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        
        try:
            while is_recording:
                data, overflowed = stream.read(1024)
                frames.append(data)
                
        except Exception as e:
            print(f"Error during recording: {e}")
        finally:
            stream.stop()
            stream.close()
            if listener.is_alive():
                listener.stop()
            
        if frames: 
            recording = np.concatenate(frames, axis=0)
            wav.write('record.wav', sample_rate, recording)
            print("\nRecording saved")
        else:
            print("\nNo audio recorded")

    record_thread = threading.Thread(target=start_recording)
    record_thread.start()

    try:
        record_thread.join()
    except KeyboardInterrupt:
        is_recording = False
        record_thread.join()
    
    return recording
