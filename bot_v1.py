import time
import pvporcupine
import pyaudio
import struct
import requests
import sounddevice as sd
import whisper
import scipy.io.wavfile as wav
import torch
import os
import psutil
import numpy as np
import json

from datetime import datetime
from TTS.api import TTS
from dotenv import load_dotenv
from rapidfuzz import process

apps = {
    "microsoft edge": "msedge",
    "edge": "msedge",
    "visual studio code": "code",
    "vs code": "code",
    "code": "code",
    "notepad": "notepad",
    "calculator": "calc",
    "firefox": "firefox",
    "mozilla": "firefox"
}

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

# ------------------- Model warmup -------------------
print("Warming up model...")

dummy_audio = np.zeros(16000, dtype=np.float32)
whisper_model.transcribe(dummy_audio)

tts.tts_to_file(text="System ready.", speaker="p226", file_path="warmup.wav")

print("Warmup complete.")


# ------------------- TTs function -------------------
def speak(text):
    print("Assistant: ", text)
    tts.tts_to_file(text=text, speaker="p226", file_path="response.wav")
    os.system("start response.wav")


# ------------------- Whisper Listen commands -------------------
def listen_command():
    print("Listening for command...")
    time.sleep(0.8)

    duration = 4
    fs = 16000

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    wav.write("input.wav", fs, recording)

    fs, audio_data = wav.read("input.wav")

    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        audio_data = audio_data / max_val

    result = whisper_model.transcribe(audio_data)
    command = result["text"].lower()

    print("You said: ", command)
    return command


# ------------------- LLM parser -------------------
def llm_parse(command):
    if len(command.strip()) < 4:
        return {"intent": "unknown"}

    prompt = f"""You are a strict JSON command parser for a PC voice assistant.
    
    You MUST respond with ONLY ONE JSON object.
    No explanations.
    No markdown.
    No code blocks.
    No extra keys.
    No text before or after JSON.
    
    Return EXACTLY one of these formats:
    
    1) {{"intent": "open_app", "app": "<app_name>"}}
    2) {{"intent": "get_time"}}
    3) {{"intent": "get_cpu"}}
    4) {{"intent": "shutdown"}}
    5) {{"intent": "unknown"}}
    
    If the command contains an app name that is NOT in the available apps list,
    Do NOT guess.
    Do NOT substitute.
    Do NOT infer.
    
    Available apps:
    - msedge
    - code
    - notepad
    - calc
    - firefox
    
    If the requested app is not in the list, return:
    {{"intent": "unknown"}}
    
    Command: "{command}"
    
    Return ONLY the JSON:
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0
                }
            }
        )

        result = response.json()["response"].strip()

        print("LLM raw response:", result)

        parsed = json.loads(result)

        return parsed
    except Exception as e:
        print("LLM parsing failed:", e)
        return {"intent": "unknown"}

# ------------------- Misheard words -------------------
def fuzzy_match_app(command):
    choices = list(apps.keys())
    match, score, _ = process.extractOne(command, choices)

    if score >= 70:
        return apps[match]
    return None

# ------------------- Multi-command parsing -------------------
def split_command(command):
    separators = [" and ", " then ", ","]
    for sep in separators:
        if sep in command:
            return command.split(sep)
    return [command]

# ------------------- Intent Parser -------------------
def parse_command(command):
    command = command.lower()

    # Open app intent
    if any(word in command for word in ["open", "start", "launch", "run"]):
        app = fuzzy_match_app(command)
        if app:
            return {"intent": "open_app"}

    # Time intent
    if "time" in command:
        return {"intent": "get_time"}

    # cpu intent
    if "cpu" in command or "usage" in command:
        return {"intent": "get_cpu"}

    # shutdown intent
    if "shutdown" in command or "turn off" in command:
        return {"intent": "shutdown"}

    return {"intent": "unknown"}

# ------------------- Safety check after parse -------------------
def safe_validate(parsed, original_command):
    if parsed["intent"] == "open_app":
        app = parsed.get("app")

        if app not in original_command:
            return {"intent": "unknown"}
    return parsed

# ------------------- Command Execute -------------------
def execute(parsed):
    intent = parsed["intent"]

    if intent == "open_app":
        app = parsed["app"]
        os.system(f"start {app}")
        reverse_app = {v: k for k, v in apps.items()}
        spoken_name = reverse_app.get(app, app)
        speak(f"Opening {spoken_name}")
    elif intent == "get_time":
        time_now = datetime.now().strftime("%H:%M")
        speak(f"The time is {time_now}")
    elif intent == "get_cpu":
        cpu = psutil.cpu_percent()
        speak(f"The cpu usage is currently {cpu} percent")
    elif intent == "shutdown":
        speak("Shutting down the system")
        os.system("shutdown /s /t 1")
    else:
        speak("I didn't understand the command.")


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

            if len(command.strip()) < 3 or command.strip() in ["yes", "yes.", "no", "okay", "ok"]:
                speak("Please say a command.")
                continue

            commands = split_command(command)

            for cmd in commands:
                parsed = parse_command(cmd.strip())

                if parsed["intent"] == "unknown":
                    parsed = llm_parse(cmd.strip())
                    parsed = safe_validate(parsed, cmd.strip())

                execute(parsed)
except KeyboardInterrupt:
    print("Stopping assistant...")
finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
