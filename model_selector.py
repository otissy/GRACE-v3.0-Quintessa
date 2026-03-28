import requests
from enum import Enum

def get_ollama_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        return []
    except Exception as e:
        print(f"Error fetching Ollama models: {e}")
        return []

def select_model():
    models = get_ollama_models()
    target_model = "hf.co/unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF:Q4_K_S"
    
    if not models:
        print("No Ollama models found. Please ensure Ollama is running.")
        return None
    
    # Priority check for the preferred model
    if target_model in models:
        print(f"\nLocked model detected: {target_model}")
        return target_model

    print("\nAvailable Ollama Models:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    print(f"\nSuggested Model: {target_model} (Not found in list)")
    choice = input(f"Select a model (1-{len(models)}) or press Enter to use {models[0]}: ").strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(models):
            return models[idx]
    
    # Default to the one that looks "latest" or just the first if no better way
    # In practice, 'latest' often means the first in the response or most recently modified
    return models[0] # Simplest for now

if __name__ == "__main__":
    selected = select_model()
    if selected:
        print(f"Using model: {selected}")
