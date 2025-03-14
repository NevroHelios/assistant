from elevenlabs import play, stream
from elevenlabs.client import ElevenLabs
import dotenv
import os

dotenv.load_dotenv()

tts_client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API")
)

def get_audio_response(text: str,
                       use_melotts: str = True,
                       voice_id: str = "XB0fDUnXU5powFXDhCwa",
                       model_id: str = "eleven_turbo_v2",
                       play_audio: bool = True):
    
    if use_melotts:
        from melo.api import TTS
        device = "auto"
        model = TTS(language="EN", device=device)
        speaker_ids = model.hps.data.spk2id
        audio_stream = model.tts_to_file(text, speaker_id=speaker_ids['EN-US'], speed=1.0, output_path="hello.wav")
    
        play(open("hello.wav", "rb"))
        return audio_stream
        
    else:
        audio_stream = tts_client.text_to_speech.convert_as_stream(
            text=text,
            voice_id=voice_id,
            model_id=model_id
        )
        
        if play_audio:
            play(audio_stream)
        return audio_stream


if __name__ == "__main__":
    from melo.api import TTS
    import soundfile as sf
    import io
    
    device = "auto"
    model = TTS(language="EN", device=device)
    speaker_ids = model.hps.data.spk2id
    audio_stream = model.tts_to_file("hello there!", speaker_id=speaker_ids['EN-US'], speed=1.0, output_path="hello.wav")
    
    play(open("hello.wav", "rb"))
    