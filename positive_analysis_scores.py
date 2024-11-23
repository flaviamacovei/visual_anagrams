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
import torch

from utils import compute_scores, model



from torch.nn.functional import softmax

def yap(text):
    with open("yap_analyse.txt", "a") as file:
        file.write(f"{text}\n")

def analyse_image(image_path, views, targets):
    score_matrix = compute_scores(image_path, views, targets).to(torch.float32)
    alignment_score = torch.min(torch.diag(score_matrix))
    yap(f"alignment: {alignment_score}")
    tau = model.logit_scale.data.item()
    concealment_score = torch.trace(softmax(score_matrix / tau)) / len(args.views)
    yap(f"concealment: {concealment_score}")
    return alignment_score > 0.7 and concealment_score > 0.7



parser = argparse.ArgumentParser()
parser.add_argument("--path", required = True, type = str, help="path to image")
parser.add_argument("--targets", required = True, type = str, nargs='+', help = "image targets (must be same length as views)")
parser.add_argument("--views", required = True, type = str, nargs='+', help = "image views (must be same length as targets)")

args = parser.parse_args()

yap(args.path)


response = analyse_image(args.path, args.views, args.targets)

sys.exit(int(response))
