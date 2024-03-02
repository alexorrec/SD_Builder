import os
import ImageManager as IM
from PIL import Image, ImageOps, ImageDraw
"""from PIL.PngImagePlugin import PngInfo
from diffusers import AutoPipelineForInpainting
from diffusers.utils import load_image
import torch.cuda
import random"""
"""
image = Image.open('D01_L1S4C3.png')
print(f"Original image size: {image.size}\n")
# _factor = int(input('Bounded Box Factor (1 - 8): '))
#c_w, c_h = image.size

r = [5]
for i in r:
    _factor = i

    crop_factor_w = int(image.width / 8 * _factor)
    crop_factor_h = int(image.height / 8 * _factor)

    crop_offset = ((image.width - crop_factor_w) // 2, (image.height - crop_factor_h) // 2,
                   (image.width + crop_factor_w) // 2, (image.height + crop_factor_h) // 2)

    print(f"_factor: {_factor}")
    print(f"crop offset: {crop_offset}")

    cropped = image.crop(crop_offset)
    print(f'CROPPED IMAGE SIZE: {cropped.size}')
    print()

    inverted_image = ImageOps.invert(cropped)
    im = Image.new('RGB', image.size, 'black')
    Image.Image.paste(im, inverted_image, crop_offset)
    im.show()
"""

"""
inpath = str(input('inpath: '))
manager = IM.ImageManager('\\', inpath)"""
"""
im = Image.open('D01_L1S4C3.png' )
c_w, c_h =

mask_size = 1024

top_left_offset = (10, 0, mask_size, mask_size)
bottom_right_offset = (c_w - mask_size, c_h - mask_size, c_w + mask_size, c_h + mask_size)

mask = Image.new(mode="RGB", size=size, color='black')
draw = ImageDraw.Draw(mask)
draw.rectangle(coordinates, fill='white')"""

path = str(input("path: "))

deleted = set()
for current, subs, files in os.walk(path, topdown=False):
    has_sub = False
    for sub in subs:
        if os.path.join(current, sub) not in deleted:
            has_sub = True
            break
    if not any(files) and not has_sub:
        os.rmdir(current)
        deleted.add(current)

print(deleted)
