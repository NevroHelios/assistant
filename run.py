from src.llm import LocalRAGPipeline
import asyncio
import time 
import threading
import keyboard
from src.tts import text_to_speech
from src.sttv2 import recognize

def run_llm(query):
    if len(query) > 1:
        query = ' '.join(query)

    async def run():
        pipeline = LocalRAGPipeline()
        model_responce = ''

        async for response in pipeline.run(query):
            model_responce += response
        return model_responce

    return asyncio.run(run())


def run_tts(text):
    text_to_speech(text)


stop_program = False

def check_for_quit():
    global stop_program
    while True:
        if keyboard.is_pressed('n'):
            stop_program = True
            print("Quitting program...")
            break
        time.sleep(0.1)







if __name__ == "__main__":
    # Start the key-checking thread
    quit_thread = threading.Thread(target=check_for_quit)
    quit_thread.daemon = True
    quit_thread.start()

    while not stop_program:
        text = recognize()  # Your voice recognition function
        print(f"voice captured: {text}")
        op = run_llm(text)  # Your LLM function
        print(f"llm response: {op}")
        text_to_speech(op)  # Your TTS function

        time.sleep(0.1)

    print("Program exited.")