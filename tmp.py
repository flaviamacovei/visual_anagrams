import os
from PIL import Image
from torchvision import transforms
from visual_anagrams.views import get_views

im_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "results/sketch/0000/sample_1024.png")
image = Image.open(im_path)
convert_tensor = transforms.ToTensor()
im_tensor = convert_tensor(image)

view_objects = get_views(["identity", "rotate_120"])

i_tensor = view_objects[0].view(im = im_tensor)
r_tensor = view_objects[1].view(im = im_tensor)

convert_pil = transforms.ToPILImage()
i_pil_image = convert_pil(i_tensor)
r_pil_image = convert_pil(r_tensor)
print(type(r_pil_image))
i_pil_image.save("i_pil_image.png")
r_pil_image.save("r_pil_image.png")

print(i_tensor.dtype)

print(r_tensor.dtype)