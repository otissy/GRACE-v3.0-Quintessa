import os
import signal
import subprocess
import time

def mouth_loop(q):
    print("--- E.D.I.T.H. Mouth Active (TTS System Ready) ---")
    current_process = None

    while True:
        try:
            cmd, text = q.get(timeout=1)
            if cmd == "SPEAK":
                # Kill existing speech if a new one starts (Interruptibility)
                if current_process and current_process.poll() is None:
                    print("Interrupting current speech...")
                    current_process.terminate()
                    current_process.wait()

                print(f"Speaking: {text}")
                # Placeholder for Qwen3-TTS usage: 
                # qwen-tts "text" or using its python API. 
                # Using a simple subproc for demonstration (replace with actual qwen call)
                # Example: current_process = subprocess.Popen(["python", "-m", "qwen_tts.cli", text])
                # Falling back to a standard TTS for now if qwen-tts cli is unknown
                current_process = subprocess.Popen(["powershell", "-Command", f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{text}')"])
            
            elif cmd == "KILL":
                if current_process and current_process.poll() is None:
                    current_process.terminate()
                    current_process.wait()
                    print("Speech killed.")

        except:
            continue

if __name__ == "__main__":
    import multiprocessing
    q = multiprocessing.Queue()
    mouth_loop(q)
