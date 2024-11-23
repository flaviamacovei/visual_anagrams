import subprocess
import requests
import base64
import time
import json
import os
import sys
# import inflect
#
# p = inflect.engine()

import argparse

from visual_anagrams.utils import add_args

# targets = ["a horse", "a snowy landscape"]

# views = {"identity": "original image",
#          "flip": "flipped along vertical axis"}

# prompt_template = (f"This image has been generated to depict an optical illusion. It has {p.number_to_words(len(goals))} "
#                  f"views and {p.number_to_words(len(goals))} corresponding goals. You can see all "
#                  f"{p.number_to_words(len(goals))} images in their corresponding view. It is your job to determine if "
#                  f"the images show \"independent synthesis\". This means that the goals are distinguishable in views "
#                  f"other than their own. If for example you can make out goal 1 in view 2, this is an indication of "
#                  f"independent synthesis. Please analyse these images and detect whether this effect occurs. Output "
#                  f"your answer in the following format:\n"
#                  f"<yes/no>---<any text or explanation>\n"
#                  f"So for example if the image shows independent synthesis, a valid output would be \"yes---I can "
#                  f"detect a rabbit in the second view, although the second goal is a goose.\"\n"
#                  f"Here are the views and goals:\n")

prompt_template = (f"This image has been generated to depict an optical illusion. It has two "
                   f"views and two corresponding goals. You can see all "
                   f"two images in their corresponding view. It is your job to determine if "
                   f"the images show \"independent synthesis\". This means that the goals are distinguishable in views "
                   f"other than their own. If for example you can make out goal 1 in view 2, this is an indication of "
                   f"independent synthesis. Please analyse these images and detect whether this effect occurs. Output "
                   f"your answer in the following format:\n"
                   f"<yes/no>---<any text or explanation>\n"
                   f"So for example if the image shows independent synthesis, a valid output would be \"yes---I can "
                   f"detect a rabbit in the second view, although the second goal is a goose.\"\n"
                   f"Here are the views and goals:\n")


def expand_prompt(prompt, views, goals):
    for i, (view, goal) in enumerate(zip(views, goals)):
        prompt += f"View {i + 1}: {view[1]}; Goal {i + 1}: {goal}\n"
    return prompt


# image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results", "horse-snow-flip", "0000", "sample_1024.views.png")

def start_ollama_server():
    try:
        subprocess.Popen(["ollama", "run", "llava"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print("Starting Ollama server with LLaVA...")
        time.sleep(5)  # wait for server to start
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

    start_time = time.time()

    response = requests.post(url, json=payload)

    end_time = time.time()

    try:
        response_lines = response.text.strip().split("\n")

        full_response = "".join(
            json.loads(line)['response'] for line in response_lines if 'response' in json.loads(line))

        return full_response, end_time - start_time
    except Exception as e:
        return f"Error: {e}"


start_ollama_server()

# print(targets)
# print(views)

# system_prompt = expand_prompt(prompt_template, views, targets)
system_prompt = (
    "Does this image contain two sub-images? Please answer the question and describe what you see. Output your answer the the following format: <yes/no>---<your description>. So for example if you don't detect two sub-images you would output \"no---the image consists of a single picture of a fish\"")

print(f"So far: {os.path.dirname(os.path.realpath(__file__))}")
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results/horse-snow-flip/0000/sample_1024.views.png")
print(f"IMAGE PATH: {image_path}")
response, compute_time = analyse_image(image_path, system_prompt)
fault_detected = response.split("---")[0].lower() == "no"

# sys.exit(int(fault_detected))
print(f"System response: {response}\nCompute time: {compute_time}")
# f = open("out.txt", "w")
# f.write(delete_images)
# f.close()
