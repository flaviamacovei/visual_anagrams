import torch
from torch.nn.functional import softmax
import clip
from PIL import Image
from visual_anagrams.views import get_views
from torchvision import transforms
import argparse
import os
from clip_utils import compute_scores, model

def yap(text):
    with open("yap_alternations.txt", "a") as file:
        file.write(f"{text}\n")


parser = argparse.ArgumentParser()
parser.add_argument("--dirnames", required = True, type=str, nargs='+')
parser.add_argument("--untils", required = True, type = int, nargs = '+')
parser.add_argument("--targets", required = True, type = str, nargs='+', help = "image targets (must be same length as views)")
parser.add_argument("--views", required = True, type = str, nargs='+', help = "image views (must be same length as targets)")
parser.add_argument("--times_path", required = True, type = str)

args = parser.parse_args()
times = []
alignment_scores = []
concealment_scores = []

for until in args.untils:
    with open("./untils.txt", "a") as file:
        file.write(f"{until}\n")


dirnames = [os.path.join(os.path.dirname(os.path.realpath(__file__)), dir, "0000/sample_1024.png") for dir in args.dirnames]
yap(dirnames)

for im_path in dirnames:
    yap(im_path)
    score_matrix = compute_scores(im_path, args.views, args.targets).to(torch.float32)
    yap(f"score matrix: {score_matrix}")
    alignment_score = torch.min(torch.diag(score_matrix))
    with open("alignments.txt", "a") as file:
        file.write(f"{alignment_score}\n")
    tau = model.logit_scale.data.item()
    concealment_score = torch.trace(softmax(score_matrix / tau)) / len(args.views)
    with open("concealments.txt", "a") as file:
        file.write(f"{concealment_score}\n")
