import subprocess
import argparse
import requests
import base64
import time
import json

def start_ollama_server():
    try:
        subprocess.Popen(["ollama", "run", "llava"], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
        print("Starting Ollama server with LLaVA...")
        time.sleep(5) # wait for server to start
    except FileNotFoundError:
        print("Error: Ollama is not installed or not in the PATH.")
        sys.exit()

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyse_image(image_path, system_prompt):
    url = "http://localhost:11434/api/generate"
    image_base64 = encode_image_to_base64(image_path)
    
    payload = {
        "model": "llava",
        "prompt": system_prompt,
        "images": [image_base64]
    }
    
    response = requests.post(url, json = payload)

    try:
        response_lines = response.text.strip().split("\n")

        full_response = "".join(json.loads(line)['response'] for line in response_lines if 'response' in json.loads(line))

        return full_response
    except Exception as e:
        return f"Error: {e}"

def parse_arguments():
    parser = argparse.ArgumentParser(description = "LLaVA Image Analysis")
    parser.add_argument("-i", "--image", required = True, help = "Path to the image file")
    parser.add_argument("-p", "--prompt", default = "Describe this image in detail", help = "System prompt for image analysis")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    start_ollama_server()
    response = analyse_image(args.image, args.prompt)
    print(f"System response: {response}")