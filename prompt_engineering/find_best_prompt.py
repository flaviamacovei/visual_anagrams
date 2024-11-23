import requests
import json
import os
import inflect
from prompt_functions import prompt_functions_is, prompt_functions_ds

p = inflect.engine()

import argparse


from ollama_utils import start_ollama_server, encode_image_to_base64

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
accuracy_ds = dict()

file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "annotations.txt")

for i in range(len(prompt_functions_is)):
    accuracy_is[i] = 0
for i in range(len(prompt_functions_ds)):
    accuracy_ds[i] = 0

with open(file_path, 'r') as file:
    for line in file:
        dirname, has_is, has_ds = line.split('---')
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
        for i in range(len(prompt_functions_ds)):
            system_prompt = prompt_functions_ds[i](views, targets)
            response = analyse_image(imagepath, system_prompt).split("---")[0].lower().strip(" <>")
            has_ds_model = (response == "yes")
            if int(has_ds_model) == int(has_ds):
                previous_score = accuracy_ds[i]
                accuracy_ds[i] = previous_score + 1

        with open("accuracies.txt", 'w') as file_acc:
            file_acc.write(f"{str(accuracy_is)}\n")
            file_acc.write(f"str(accuracy_ds)")
