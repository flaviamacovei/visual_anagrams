import sys
import torch


try:
    from utilities.clip_utils import compute_alignment, compute_concealment, compute_dispersion
except ImportError:
    import sys
    sys.path.append(sys.path[0] + '/..')
    from utilities.clip_utils import compute_alignment, compute_concealment, compute_dispersion
import argparse


def yap(text):
    with open("yap.txt", "a") as file:
        file.write(f"{text}\n")

def analyse_image_is(image_path, views, targets):
    alignment_score = compute_alignment(image_path, views, targets)
    concealment_score = compute_concealment(image_path, views, targets)
    yap(f"alignment score: {alignment_score}\nconcealment score: {concealment_score}")
    is_score = concealment_score / alignment_score

    return is_score < 0.56


def analyse_image_ds(image_path, views, targets):
    dispersion_score = compute_dispersion(image_path, views, targets)
    yap(f"disperson_score: {dispersion_score}")
    return dispersion_score < 0.2



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required = True, type = str, help="path to image")
    parser.add_argument("--targets", required = True, type = str, nargs='+', help = "image targets (must be same length as views)")
    parser.add_argument("--views", required = True, type = str, nargs='+', help = "image views (must be same length as targets)")
    parser.add_argument("--fault", required = True, type = str, help = "fault to be detected: is (independent synthesis) or ds (solitary synthesis)")

    args = parser.parse_args()

    yap(args.path)

    if args.fault == "is":
        fault_detected = analyse_image_is(args.path, args.views, args.targets)
    else:
        fault_detected = analyse_image_ds(args.path, args.views, args.targets)


    sys.exit(int(fault_detected))
