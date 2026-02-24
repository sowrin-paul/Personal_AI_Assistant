import pvporcupine
import pyaudio
import struct
import sounddevice as sd
import whisper
import scipy.io.wavfile as wav
import torch
import os
import psutil
import numpy as np
from datetime import datetime
from TTS.api import TTS
from dotenv import load_dotenv

load_dotenv()

# ------------------- Init -------------------
ACCESS_KEY = os.getenv("ACCESS_KEY")
if not ACCESS_KEY:
    raise ValueError("ACCESS_KEY not found in the env file.")

WAKE_WORD = ["sarvis"]

# ------------------- Init Model -------------------
print("Loading Whisper Model...")
whisper_model = whisper.load_model("base")

print("Loading tts model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/en/vctk/vits").to(device)

# ------------------- TTs function -------------------
def speak(text):
    print("Assistant: ", text)
    tts.tts_to_file(text=text, speaker="p226", file_path="response.wav")
    os.system("start response.wav")

# ------------------- Whisper Listen commands -------------------
def listen_command():
    print("Listening for command...")

    duration = 4
    fs = 16000

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    wav.write("input.wav", fs, recording)

    fs, audio_data = wav.read("input.wav")

    audio_data = audio_data.astype(np.float32).flatten()
    audio_data = audio_data / np.max(np.abs(audio_data))

    result = whisper_model.transcribe(audio_data)
    command = result["text"].lower()

    print("You said: ", command)
    return command

# ------------------- Command Execute -------------------
def execute(command):

    if "open edge" in command:
        os.system("start msedge")
        speak("Opening edge")
    elif "open code" in command or "open vs code" in command:
        os.system("code")
        speak("Opening Visual Studio Code")
    elif "time" in command:
        time_now = datetime.now().strftime("%H:%M")
        speak(f"The time is {time_now}")
    elif "cpu usage" in command:
        cpu = psutil.cpu_percent()
        speak(f"The cpu usage is currently {cpu}")
    elif "shutdown" in command:
        speak("Shutting down the system")
        os.system("shutdown /s /t 1")
    else:
        speak("I don't understand yet.")

# ------------------- Wake Word loop -------------------
print("Loading wake word engine...")

keyword_path = os.path.join(os.path.dirname(__file__), "Sarvis_en_windows_v4_0_0.ppn")
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[keyword_path]
)

pa = pyaudio.PyAudio()

audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("Assistant is running...Say 'Sarvis'")

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Wake word detected!")
            speak("Yes?")
            command = listen_command()
            execute(command)
except KeyboardInterrupt:
    print("Stopping assistant...")
finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()