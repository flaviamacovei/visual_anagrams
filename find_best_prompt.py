import subprocess
import requests
import base64
import time
import json
import os
import sys
import inflect
from prompt_functions import prompt_functions_is, prompt_functions_ss

p = inflect.engine()

import argparse


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


def recover_phrases(line):
    targets_str = line.split("-")[0]
    targets_str = targets_str[2:]
    targets = [i.replace("_", " ") for i in targets_str.split("_a_")]

    return targets

start_ollama_server()

accuracy_is = dict()
# accuracy_ss = dict()

file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "annotations.txt")

for i in range(len(prompt_functions_is)):
    accuracy_is[i] = 0
# for i in range(len(prompt_functions_ss)):
#     accuracy_ss[i] = 0

with open(file_path, 'r') as file:
    for line in file:
        dirname, has_is, has_ss = line.split('---')
        targets = recover_phrases(line)
        views = ["identity", dirname.split('-')[-1][:-1].replace("_", " ")]
        imagepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"results/{dirname}/0000/sample_1024.views.png")
        for i in range(len(prompt_functions_is)):
            system_prompt = prompt_functions_is[i](views, targets)
            response = analyse_image(imagepath, system_prompt).split("---")[0].lower().strip(" <>")
            has_is_model = (response == "yes")
            if int(has_is_model) == int(has_is):
                previous_score = accuracy_is[i]
                accuracy_is[i] = previous_score + 1
        # for i in range(len(prompt_functions_ss)):
        #     system_prompt = prompt_functions_ss[i](views, targets)
        #     response = analyse_image(imagepath, system_prompt).split("---")[0].lower().strip(" <>")
        #     has_ss_model = (response == "yes")
        #     if int(has_ss_model) == int(has_ss):
        #         previous_score = accuracy_ss[i]
        #         accuracy_ss[i] = previous_score + 1

        with open("accuracies.txt", 'w') as file_acc:
            file_acc.write(str(accuracy_is))
            # file_acc.write(str(accuracy_ss))
