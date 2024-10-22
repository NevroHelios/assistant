import requests
import json
import time
import os

def text_to_speech(text, verbose=True):
    def request_synthesis(text):
        base_url = "http://127.0.0.1:7860"
        endpoint = "/queue/join"
        payload = json.dumps({
            "data": ["EN-US", text, 1, "EN"],
            "event_data": None,
            "fn_index": 1,
            "trigger_id": 8,
            "session_hash": "60236rt7l1u"
        })
        
        url = base_url + endpoint
        req = requests.post(url, payload)
        return req.json()

    def get_folder(url="http://127.0.0.1:5070", max_retries=20, delay=0.5, first=False):
        if first:
            return requests.get(url).json()['latest_folder']
        return requests.get(url).json()['latest_folder']

    def get_audio(folder_name, max_retries=20, delay=0.5):
        url = f"http://127.0.0.1:7860/file=/tmp/gradio/{folder_name}/audio"
        req = requests.get(url)
        return req.content

    def to_file(audio, file_name="temp"):
        audio_file = f"{file_name}.wav"
        with open(audio_file, "wb") as f:
            f.write(audio)
        return audio_file

    def play(audio_file):
        import sounddevice as sd
        import soundfile as sf
        data, fs = sf.read(audio_file)
        sd.play(data, fs)
        sd.wait()

    try:
        initial_folder = get_folder(first=True)
        if verbose: print(f"Initial folder: {initial_folder}")

        job_hash = request_synthesis(text)
        if verbose: print(f"Job hash: {job_hash}")
        
        # Wait for a new folder
        new_folder = initial_folder
        max_retries = 30
        for _ in range(max_retries):
            time.sleep(1)
            new_folder = get_folder()
            if new_folder != initial_folder:
                break
        
        if new_folder == initial_folder:
            raise Exception("No new folder detected after maximum retries")
        
        if verbose: print(f"New folder detected: {new_folder}")
        
        audio = get_audio(new_folder)
        audio_file = to_file(audio=audio)
        play(audio_file)
        return "success"
    except Exception as e:
        print(f"Error: {e}")
        return "failed"



if __name__ == "__main__":
    # Example usage
    para = \
    """
    The sun was setting over the bustling streets of Tokyo, casting a warm orange glow over the crowded sidewalks. The
    sound of laughter and chatter filled the air as people made their way home from work or out for dinner with
    friends. In the midst of this vibrant scene, a small group of street performers had gathered on the corner of a
    quiet side street, drawing in a crowd with their lively music and acrobatic tricks. A young musician, perched on
    top of a stack of boxes, strummed the strings of his guitar with infectious energy, while a pair of jugglers
    expertly kept three glowing balls aloft as they weaved through the gathering crowd. As the sun dipped below the
    horizon, the performers paused to take a bow, their faces flushed with excitement and admiration from the
    delighted onlookers.
    """
    result = text_to_speech(para)
    print(result)