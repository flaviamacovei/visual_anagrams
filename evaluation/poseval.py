import sys
import argparse

import torch

try:
    from utilities.clip_utils import compute_alignment, compute_concealment, compute_dispersion
except ImportError:
    import sys
    sys.path.append(sys.path[0] + '/..')
    from utilities.clip_utils import compute_alignment, compute_concealment, compute_dispersion


def analyse_image(image_path, views, targets):
    alignment_score = compute_alignment(image_path, views, targets)
    concealment_score = compute_concealment(image_path, views, targets)
    dispersion_score = compute_dispersion(image_path, views, targets)
    return alignment_score >= 0.7 and concealment_score >= 0.7 and dispersion_score >= 0.5


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required = True, type = str, help="path to image")
    parser.add_argument("--targets", required = True, type = str, nargs='+', help = "image targets (must be same length as views)")
    parser.add_argument("--views", required = True, type = str, nargs='+', help = "image views (must be same length as targets)")
    
    args = parser.parse_args()
    
    
    response = analyse_image(args.path, args.views, args.targets)
    
    sys.exit(int(response))
