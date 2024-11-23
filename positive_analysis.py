import subprocess
import requests
import base64
import time
import json
import os
import sys
import inflect
from torchvision import transforms
from PIL import Image
import io
import argparse

from visual_anagrams.views import get_views

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

def analyse_image(image_path, system_prompt, views, targets):
    url = "http://localhost:11434/api/generate"
    view_objects = get_views(views, None)
    image = Image.open(image_path)
    convert_tensor = transforms.ToTensor()
    img_tensor = convert_tensor(image)
    for i in range(len(view_objects)):
        viewed_image = view_objects[i].view(im = img_tensor)
        convert_pil = transforms.ToPILImage()
        pil_image = convert_pil(viewed_image)
        buffer = io.BytesIO()
        pil_image.save(buffer, format = 'PNG')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        viewed_system_prompt = system_prompt.format(target = targets[i])

        payload = {
            "model": "llava",
            "prompt": viewed_system_prompt,
            "images": [image_base64]
        }
        response = requests.post(url, json = payload)
    
        try:
            response_lines = response.text.strip().split("\n")

            full_response = "".join(json.loads(line)['response'] for line in response_lines if 'response' in json.loads(line))
            print(f"RESPONSE: {full_response.lower().strip(' <>.')}")

            if full_response.lower().strip(" <>.") != "yes":
                return False
        except Exception as e:
            return f"Error: {e}"
    return True


start_ollama_server()

parser = argparse.ArgumentParser()
parser.add_argument("--path", required = True, type = str, help="path to image")
parser.add_argument("--targets", required = True, type = str, nargs='+', help = "image targets (must be same length as views)")
parser.add_argument("--views", required = True, type = str, nargs='+', help = "image views (must be same length as targets)")

args = parser.parse_args()


system_prompt = ("This is an artificially generated image. Is there {target} in it? Be very strict in your judgement.\n"
                 "Output your answer as \"yes\" or \"no\", no additional text or explanation.")

response = analyse_image(args.path, system_prompt, args.views, args.targets)

sys.exit(response)
