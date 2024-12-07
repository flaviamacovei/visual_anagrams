import torch
from torch.nn.functional import softmax
import argparse
import os
from clip_utils import compute_alignment, compute_concealment


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

result_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "results_alternations")


for until in args.untils:
    with open(f"{result_dir}/untils.txt", "a") as file:
        file.write(f"{until}\n")



dirnames = [os.path.join(os.path.dirname(os.path.realpath(__file__)), dir, "0000/sample_1024.png") for dir in args.dirnames]

for im_path in dirnames:
    alignment_score = compute_alignment(im_path, args.views, args.targets)
    with open(f"{result_dir}/alignments.txt", "a") as file:
        file.write(f"{alignment_score}\n")
    concealment_score = compute_concealment(im_path, args.views, args.targets)
    with open(f"{result_dir}/concealments.txt", "a") as file:
        file.write(f"{concealment_score}\n")
