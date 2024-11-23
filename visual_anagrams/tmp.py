from PIL import Image
import torch
from views.view_base import BaseView

class IdentityView(BaseView):
    def __init__(self):
        pass

    def view(self, im):
        return im

    def inverse_view(self, noise):
        return noise


class FlipView(BaseView):
    def __init__(self):
        pass

    def view(self, im):
        return torch.flip(im, [1])

    def inverse_view(self, noise):
        return torch.flip(noise, [1])

    def make_frame(self, im, t):
        im_size = im.size[0]
        frame_size = int(im_size * 1.5)
        theta = -t * 180

        # TODO: Technically not a flip, change this to a homography later
        frame = Image.new('RGB', (frame_size, frame_size), (255, 255, 255))
        frame.paste(im, ((frame_size - im_size) // 2, (frame_size - im_size) // 2))
        frame = frame.rotate(theta,
                             resample=Image.Resampling.BILINEAR,
                             expand=False,
                             fillcolor=(255,255,255))

        return frame

VIEW_MAP = {
    'identity': IdentityView,
    'flip': FlipView,
}

def get_views(view_names, view_args=None):
    '''
    Bespoke function to get views (just to make command line usage easier)
    '''

    views = []
    if view_args is None:
        view_args = [None for _ in view_names]

    for view_name, view_arg in zip(view_names, view_args):
        if view_name == 'patch_permute':
            args = [8 if view_arg is None else int(view_arg)]
        elif view_name == 'pixel_permute':
            args = [64 if view_arg is None else int(view_arg)]
        elif view_name == 'skew':
            args = [1.5 if view_arg is None else float(view_arg)]
        elif view_name in ['low_pass', 'high_pass']:
            args = [2.0 if view_arg is None else float(view_arg)]
        elif view_name in ['scale']:
            args = [0.5 if view_arg is None else float(view_arg)]
        else:
            args = []

        view = VIEW_MAP[view_name](*args)
        views.append(view)

    return views

v = get_views(["identity", "flip"])
print(v)
