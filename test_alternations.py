import torch
from torch.nn.functional import softmax
import clip
from PIL import Image
from visual_anagrams.views import get_views
from torchvision import transforms
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def yap(text):
    with open("yap.txt", "a") as file:
        file.write(f"{text}\n")

yap("here we go")

def compute_scores(image_path, views, prompts):
    scores = []
    view_objects = get_views(views, None)
    image = Image.open(image_path)
    convert_tensor = transforms.ToTensor()
    img_tensor = convert_tensor(image)
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
    return score_matrix

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
    with open("untils.txt", "a") as file:
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
    # alignment_scores.append(alignment_score.item())
    tau = model.logit_scale.data.item()
    concealment_score = torch.trace(softmax(score_matrix / tau)) / len(args.views)
    with open("concealments.txt", "a") as file:
        file.write(f"{concealment_score}\n")
    # concealment_scores.append(concealment_score.item())

# print(f"alignment scores: {alignment_scores}")
# print(f"concealment scores: {concealment_scores}")
# print(f"untils: {args.untils}")
# print(f"times: {times}")
# untils on x axis, times on y axis, alignment / concealment score as heatmap


