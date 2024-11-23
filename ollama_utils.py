import subprocess
import time
import sys
import base64



def start_ollama_server():
    try:
        subprocess.Popen(["ollama", "run", "llava"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        # print("Starting Ollama server with LLaVA...")
        time.sleep(5) # wait for server to start
    except FileNotFoundError:
        print("Error: Ollama is not installed or not in the PATH.")
        sys.exit()

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
