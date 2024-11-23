import sys
import torch
from clip_utils import compute_scores



import argparse


def yap(text):
    with open("yap2.txt", "a") as file:
        file.write(f"{text}\n")



def analyse_image_is(image_path, views, targets):
    score_matrix = compute_scores(image_path, views, targets).to(torch.float32)
    alignment_score = torch.min(torch.diag(score_matrix))

    yap(alignment_score)

    misalignment_score = torch.min(torch.diag(score_matrix[:, [1, 0]]))
    yap(misalignment_score)
    is_score = alignment_score / misalignment_score

    yap(f"is score: {is_score}")

    return is_score < 10


def analyse_image_ds(image, views, targets):
    score_matrix = compute_scores(image, views, targets).to(torch.float32)
    highest = torch.argmax(score_matrix, dim = 1)
    yap(f"highest: {highest}")

    has_ds = torch.all(highest == highest[0])

    yap(f"has ds: {has_ds}")

    return has_ds



if __name__ == "__main__":
    yap("starting analysis")
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required = True, type = str, help="path to image")
    parser.add_argument("--targets", required = True, type = str, nargs='+', help = "image targets (must be same length as views)")
    parser.add_argument("--views", required = True, type = str, nargs='+', help = "image views (must be same length as targets)")
    parser.add_argument("--fault", required = True, type = str, help = "fault to be detected: is (independent synthesis) or ds (solitary synthesis)")

    args = parser.parse_args()

    if args.fault == "is":
        fault_detected = analyse_image_is(args.path, args.views, args.targets)
    else:
        fault_detected = analyse_image_ds(args.path, args.views, args.targets)


    sys.exit(int(fault_detected))
