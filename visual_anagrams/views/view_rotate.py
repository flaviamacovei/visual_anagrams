import torch
from PIL import Image, ImageDraw, ImageFilter
import torchvision.transforms.functional as TF
from torchvision.transforms import InterpolationMode

import torchvision.transforms.functional as TF
from torchvision.transforms import InterpolationMode

from .view_base import BaseView


class Rotate90CWView(BaseView):
    def __init__(self):
        pass

    def view(self, im):
        # TODO: Is nearest-exact better?
        return TF.rotate(im, -90, interpolation=InterpolationMode.NEAREST)

    def inverse_view(self, noise):
        return TF.rotate(noise, 90, interpolation=InterpolationMode.NEAREST)

    def make_frame(self, im, t):
        im_size = im.size[0]
        frame_size = int(im_size * 1.5)
        theta = t * -90

        frame = Image.new('RGB', (frame_size, frame_size), (255, 255, 255))
        centered_loc = (frame_size - im_size) // 2
        frame.paste(im, (centered_loc, centered_loc))
        frame = frame.rotate(theta,
                             resample=Image.Resampling.BILINEAR,
                             expand=False,
                             fillcolor=(255,255,255))

        return frame


class Rotate90CCWView(BaseView):
    def __init__(self):
        pass

    def view(self, im):
        # TODO: Is nearest-exact better?
        return TF.rotate(im, 90, interpolation=InterpolationMode.NEAREST)

    def inverse_view(self, noise):
        return TF.rotate(noise, -90, interpolation=InterpolationMode.NEAREST)

    def make_frame(self, im, t):
        im_size = im.size[0]
        frame_size = int(im_size * 1.5)
        theta = t * 90

        frame = Image.new('RGB', (frame_size, frame_size), (255, 255, 255))
        centered_loc = (frame_size - im_size) // 2
        frame.paste(im, (centered_loc, centered_loc))
        frame = frame.rotate(theta,
                             resample=Image.Resampling.BILINEAR,
                             expand=False,
                             fillcolor=(255,255,255))

        return frame


class Rotate180View(BaseView):
    def __init__(self):
        pass

    def view(self, im):
        # TODO: Is nearest-exact better?
        rotated = TF.rotate(im, 180, interpolation=InterpolationMode.NEAREST)
        return rotated

    def inverse_view(self, noise):
        rotated = TF.rotate(noise, -180, interpolation=InterpolationMode.NEAREST)
        return rotated

    def make_frame(self, im, t):
        im_size = im.size[0]
        frame_size = int(im_size * 1.5)
        theta = t * 180

        frame = Image.new('RGB', (frame_size, frame_size), (255, 255, 255))
        centered_loc = (frame_size - im_size) // 2
        frame.paste(im, (centered_loc, centered_loc))
        frame = frame.rotate(theta,
                             resample=Image.Resampling.BILINEAR,
                             expand=False,
                             fillcolor=(255,255,255))

        return frame


class RotateView120(BaseView):
    def __init__(self):
        """
        Initialize with the rotation angle (120 or 240 degrees).
        :param angle: Rotation angle in degrees (positive for clockwise).
        """
        self.angle = 120

    def apply_circular_mask(self, im):
        """Applies a circular mask to the image."""
        c, h, w = im.shape
        assert h == w, "Image must be square for proper circular masking."
        y, x = torch.meshgrid(
            torch.linspace(-1, 1, h),
            torch.linspace(-1, 1, w),
            indexing="ij"
        )
        mask = (x**2 + y**2 <= 1).float().to(im.device)  # Circle mask
        return im * mask.unsqueeze(0).expand(c, -1, -1)  # Apply mask to all channels

    def view(self, im):
        """
        Rotate the image clockwise by the specified angle.
        :param im: Input tensor or PIL Image
        :return: Rotated image
        """

        # Apply circular mask
        im = self.apply_circular_mask(im)

        # Perform rotation
        num_channels = im.shape[0]
        fill = (0,) * num_channels
        rotated_im = TF.rotate(im, -self.angle, interpolation=InterpolationMode.BILINEAR, fill = fill).to(torch.float16)
        return rotated_im

    def inverse_view(self, noise):
        """
        Rotate the image counterclockwise by the specified angle.
        :param noise: Input tensor or PIL Image
        :return: Inverse-rotated image
        """

        # Apply circular mask
        rotated_noise = self.apply_circular_mask(noise)

        # Perform rotation
        num_channels = noise.shape[0]
        fill = (0,) * num_channels
        rotated_noise = TF.rotate(noise, self.angle, interpolation=InterpolationMode.BILINEAR, fill = fill).to(torch.float16)
        return rotated_noise

    def make_frame(self, im, t):
        """
        Create a frame for visualization.
        :param im: PIL Image
        :param t: Time/frame factor for dynamic rotation
        :return: Framed and rotated PIL Image
        """
        im_size = im.size[0]
        frame_size = int(im_size * 1.5)
        theta = t * -self.angle

        # Create the frame and paste the masked image
        frame = Image.new('RGB', (frame_size, frame_size), (255, 255, 255))
        centered_loc = (frame_size - im_size) // 2
        frame.paste(im, (centered_loc, centered_loc))

        # Apply rotation and circular mask
        frame_tensor = TF.to_tensor(frame)
        frame_tensor = self.apply_circular_mask(frame_tensor)

        return TF.to_pil_image(frame_tensor)

class RotateView240(BaseView):
    def __init__(self):
        """
        Initialize with the rotation angle (120 or 240 degrees).
        :param angle: Rotation angle in degrees (positive for clockwise).
        """
        self.angle = 240

    def apply_circular_mask(self, im):
        """Applies a circular mask to the image."""
        c, h, w = im.shape
        assert h == w, "Image must be square for proper circular masking."
        y, x = torch.meshgrid(
            torch.linspace(-1, 1, h),
            torch.linspace(-1, 1, w),
            indexing="ij"
        )
        mask = (x**2 + y**2 <= 1).float().to(im.device)  # Circle mask
        return im * mask.unsqueeze(0).expand(c, -1, -1)  # Apply mask to all channels

    def view(self, im):
        """
        Rotate the image clockwise by the specified angle.
        :param im: Input tensor or PIL Image
        :return: Rotated image
        """

        # Apply circular mask
        im = self.apply_circular_mask(im)

        # Perform rotation
        num_channels = im.shape[0]
        fill = (0,) * num_channels
        rotated_im = TF.rotate(im, -self.angle, interpolation=InterpolationMode.BILINEAR, fill = fill).to(torch.float16)
        return rotated_im

    def inverse_view(self, noise):
        """
        Rotate the image counterclockwise by the specified angle.
        :param noise: Input tensor or PIL Image
        :return: Inverse-rotated image
        """

        # Apply circular mask
        rotated_noise = self.apply_circular_mask(noise)

        # Perform rotation
        num_channels = noise.shape[0]
        fill = (0,) * num_channels
        rotated_noise = TF.rotate(noise, self.angle, interpolation=InterpolationMode.BILINEAR, fill = fill).to(torch.float16)
        return rotated_noise

    def make_frame(self, im, t):
        """
        Create a frame for visualization.
        :param im: PIL Image
        :param t: Time/frame factor for dynamic rotation
        :return: Framed and rotated PIL Image
        """
        im_size = im.size[0]
        frame_size = int(im_size * 1.5)
        theta = t * -self.angle

        # Create the frame and paste the masked image
        frame = Image.new('RGB', (frame_size, frame_size), (255, 255, 255))
        centered_loc = (frame_size - im_size) // 2
        frame.paste(im, (centered_loc, centered_loc))

        # Apply rotation and circular mask
        frame_tensor = TF.to_tensor(frame)
        frame_tensor = self.apply_circular_mask(frame_tensor)

        return TF.to_pil_image(frame_tensor)
