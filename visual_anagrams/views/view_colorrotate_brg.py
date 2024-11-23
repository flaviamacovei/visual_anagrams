from PIL import Image
import numpy as np

import torch

from .view_base import BaseView

class ColorRotate_BRG(BaseView):
    def __init__(self):
        pass

    def view(self, im):
        new_ims = []
        for i in range(0, im.shape[0], 3):
            new_ims.append(torch.stack([im[i + 2, :, :], im[i, :, :], im[i + 1, :, :]]))
        return torch.cat(new_ims)

    def inverse_view(self, noise):
        '''
        Negating the variance estimate is "weird" so just don't do it.
            This hack seems to work just fine
        '''
        new_noises = []
        for i in range(0, noise.shape[0], 3):
            new_noises.append(torch.stack([noise[i + 1, :, :], noise[i + 2, :, :], noise[i, :, :]]))
        return torch.cat(new_noises)
        # invert_mask = torch.ones_like(noise)
        # invert_mask[:3] = -1
        # return noise * invert_mask

    def make_frame(self, im, t):
        im_size = im.size[0]
        frame_size = int(im_size * 1.5)

        # map t from [0, 1] -> [1, -1]
        t = 1 - t
        t = t * 2 - 1

        # Interpolate from pixels from [0, 1] to [1, 0]
        im = np.array(im) / 255.
        im = ((2 * im - 1) * t + 1) / 2.
        im = Image.fromarray((im * 255.).astype(np.uint8))

        # Paste on to canvas
        frame = Image.new('RGB', (frame_size, frame_size), (255, 255, 255))
        frame.paste(im, ((frame_size - im_size) // 2, (frame_size - im_size) // 2))

        return frame
