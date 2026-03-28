import os
import sys
import time
import queue
import json
import pyaudio
from vosk import Model, KaldiRecognizer

def ear_loop(q):
    # Load model from local models directory if available
    model_path = r"c:\Users\31615\Desktop\GRACE\models\vosk-model-small-en-us-0.15"
    if not os.path.exists(model_path):
        print(f"Vosk model not found at {model_path}. Please download it.")
        return

    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print("--- E.D.I.T.H. Ear Active (Listening for 'Edith' or 'Quintessa') ---")
    
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").lower()
            if text:
                print(f"Captured: {text}")
                # Check for wake word
                if "edith" in text or "quintessa" in text:
                    print("Wake word detected!")
                    q.put(("WAKE", text))
                else:
                    q.put(("INPUT", text))

if __name__ == "__main__":
    # Test stub
    import multiprocessing
    q = multiprocessing.Queue()
    ear_loop(q)
