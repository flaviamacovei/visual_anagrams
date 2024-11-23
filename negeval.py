import requests
import json
import sys
import inflect
from ollama_utils import start_ollama_server, encode_image_to_base64

p = inflect.engine()

import argparse


def create_system_prompt_is(goals):
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

def create_system_prompt_ds(goals):
    prompt = (f"This image consits of {p.number_to_words(len(goals))} subimages. You will be given a list of targets that "
            f"correspond to each subimage. Your objective is to detect if the image shows signs of \"dominant synthesis\" "
            f"which means that one target is achieved to a significantly higher degree than the others. One indication is "
            f"that you can discern a target in a subimage other than its corresponding one. It would also be that for one "
            f"sub-image, you can't depict its target in it. Please analyze the image and tell me if you detect dominant "
            f"synthesis. It is important that you output your response in the following format:\n"
            f"<yes/no>---<any text or explanation>\n"
            f"For example: \"yes---the first target of a horse is much more pronounced than the other target.\"\n"
            f"Here are the target images:\n")
    for i, goal in enumerate(goals):
        prompt += f"Subimage {i + 1}: {goal}\n"
    return prompt


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


if __name__ == "__main__":
    start_ollama_server()

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required = True, type = str, help="path to image")
    parser.add_argument("--targets", required = True, type = str, nargs='+', help = "image targets (must be same length as views)")
    parser.add_argument("--views", required = True, type = str, nargs='+', help = "image views (must be same length as targets)")
    parser.add_argument("--fault", required = True, type = str, help = "fault to be detected: is (independent synthesis) or ds (dominant synthesis)")

    args = parser.parse_args()

    if args.fault == "is":
        prompt_fn = create_system_prompt_is
    else:
        prompt_fn = create_system_prompt_ds


    system_prompt = prompt_fn(args.targets)

    response = analyse_image(args.path, system_prompt)
    fault_detected = response.split("---")[0].lower().strip(" <>") == "no"

    sys.exit(int(fault_detected))
