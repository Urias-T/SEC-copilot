import pyaudio 
import wave
import io
import os


import openai

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

FRAMES_PER_BUFFER = 3200 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


def listen():
    sound = pyaudio.PyAudio()

    stream = sound.open(
        format=FORMAT,
        rate=RATE,
        channels=CHANNELS,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    print("Start recording")

    seconds = 5
    frames=[]

    for i in range (0, int(RATE/FRAMES_PER_BUFFER*seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    sound.terminate()

    obj = wave.open("query.wav", "wb")
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(sound.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))
    obj.close()

    with open("query.wav", "rb") as audio_file:
        transcript = openai.Audio.transcribe(
            file=audio_file,
            model="whisper-1",
            response_format="text",
            language="en"
        )

    print(transcript)

    return(transcript)

