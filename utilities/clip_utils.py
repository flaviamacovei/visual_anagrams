from torchvision import transforms
from PIL import Image
import clip
import torch
from torch.nn.functional import softmax

try:
    from visual_anagrams.views import get_views
except ImportError:
    import sys
    sys.path.append(sys.path[0] + '/..')
    from visual_anagrams.views import get_views


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)



def compute_scores(image_path, views, prompts):
    assert len(views) == len(prompts)
    yap(image_path)
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

def compute_alignment(image_path, views, prompts):
    score_matrix = compute_scores(image_path, views, prompts).to(torch.float32)
    return torch.min(torch.diag(score_matrix))

def compute_concealment(image_path, views, prompts):
    score_matrix = compute_scores(image_path, views, prompts).to(torch.float32)
    tau = model.logit_scale.data.item()
    return torch.trace(softmax(score_matrix / tau)) / len(views)

def compute_dispersion(image_path, views, prompts):
    score_matrix = compute_scores(image_path, views, prompts).to(torch.float32)
    variance = torch.var(score_matrix.argmax(dim = 1).float())
    return variance / len(views)