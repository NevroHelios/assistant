import pyaudio
import keyboard

chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 44100
seconds = 2
filename = "output.wav"

frames = []

from faster_whisper import WhisperModel
model = WhisperModel("base", device="cuda", compute_type="float16")

def record():
    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    print("Recording...")
    while True:
        data = stream.read(chunk)
        frames.append(data)

        if keyboard.is_pressed('q'):
            break


    stream.stop_stream()
    stream.close()
    p.terminate()

def recognize():
    record()

    import wave
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))

    segments, info = model.transcribe(filename, beam_size=5)

    transcribtions = [segment.text for segment in segments]
    frames.clear()
    return transcribtions
