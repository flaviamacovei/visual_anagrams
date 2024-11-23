import subprocess
import requests
import time
import json
import os
import sys
from torchvision import transforms
import argparse
import numpy as np

from PIL import Image


import clip


from torch.nn.functional import softmax

import torch

from visual_anagrams.views import get_views


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)



def yap(text):
    with open("yap_score_matrix.txt", "a") as file:
        file.write(f"{text}\n")

def compute_scores(image_path, views, prompts):
    scores = []
    view_objects = get_views(views, None)
    image = Image.open(image_path)
    convert_tensor = transforms.ToTensor()
    img_tensor = convert_tensor(image)
    yap(f"image tensor shape: {img_tensor.shape}")
    prompts_tokenised = clip.tokenize(prompts).to(device)
    with torch.no_grad():
        prompts_features = model.encode_text(prompts_tokenised)
    for view in view_objects:
        viewed_image = view.view(im=img_tensor)
        convert_pil = transforms.ToPILImage()
        pil_image = preprocess(convert_pil(viewed_image)).unsqueeze(0).to(device)

        with torch.no_grad():
            image_features = model.encode_image(pil_image)
            logits_per_image, logits_per_text = model(pil_image, prompts_tokenised)
            probs = logits_per_image.softmax(dim=-1).cpu()
            scores.append(probs[0])
    score_matrix = torch.stack(scores)
    yap(f"score matrix: {score_matrix}")
    return score_matrix