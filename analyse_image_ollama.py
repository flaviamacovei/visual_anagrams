import subprocess
import requests
import base64
import time
import json
import os
import sys
import inflect

p = inflect.engine()

import argparse


def create_system_prompt_is(views, goals):
    prompt = (f"You are analyzing an image that has been split into {p.number_to_words(len(goals))} subimages. "
              f"Each subimage corresponds to a target. Your task is to evaluate if all target images are detectable "
              f"in all subimages. This phenomenon is referred to as \"independent synthesis.\" For each subimage, "
              f"check if it contains a target image that belongs to a different subimage.\n"
              f"Provide your output as follows: <yes/no>---<any text or explanation>\n"
              f"For example: \"yes---I can detect both a rabbit and a goose in both subimages.\"\n"
              f"Here are the target images:\n")
    for i, goal in enumerate(goals):
        prompt += f"Subimage {i + 1}: {goal}\n"
    return prompt

def create_system_prompt_ss(views, goals):
    prompt = (f"This image conssits of {p.number_to_words(len(goals))} subimages. You will be given a list of targets that "
            f"correspond to each subimage. Your objective is to detect if the image shows signs of \"solitary synthesis\" "
            f"which means that one target is achieved to a significantly higher degree than the others. One indication is "
            f"that you can discern a target in a subimage other than its corresponding one. It would also be that for one "
            f"sub-image, you can't depict its target in it. Please analyze the image and tell me if you detect solitary "
            f"synthesis. It is important that you output your response in the following format:\n"
            f"<yes/no>---<any text or explanation>\n"
            f"For example: \"yes---the first target of a horse is much more pronounced than the other target.\"\n"
            f"Here are the target images:\n")
    for i, goal in enumerate(goals):
        prompt += f"Subimage {i + 1}: {goal}\n"
    return prompt


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


start_ollama_server()

parser = argparse.ArgumentParser()
parser.add_argument("--path", required = True, type = str, help="path to image")
parser.add_argument("--targets", required = True, type = str, nargs='+', help = "image targets (must be same length as views)")
parser.add_argument("--views", required = True, type = str, nargs='+', help = "image views (must be same length as targets)")
parser.add_argument("--fault", required = True, type = str, help = "fault to be detected: is (independent synthesis) or ss (solitary synthesis)")

args = parser.parse_args()

if args.fault == "is":
    prompt_fn = create_system_prompt_is
else:
    prompt_fn = create_system_prompt_ss


system_prompt = prompt_fn(args.views, args.targets)

response = analyse_image(args.path, system_prompt)
fault_detected = response.split("---")[0].lower().strip(" <>") == "no"

sys.exit(int(fault_detected))
