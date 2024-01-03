import os
import ImageManager as IM
from PIL import Image, ImageOps
"""from PIL.PngImagePlugin import PngInfo
from diffusers import AutoPipelineForInpainting
from diffusers.utils import load_image
import torch.cuda
import random"""
"""
image = Image.open('DJI_0499-TESTING.jpg')
print(f"Original image size: {image.size}\n")
# _factor = int(input('Bounded Box Factor (1 - 8): '))
#c_w, c_h = image.size

r = [8]
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
    #inverted_image.show()
    Image.Image.paste(image, inverted_image, crop_offset)
    image.show()

"""


manager = IM.ImageManager('\\', '/Users/alessandrocerro/Desktop/Export_WEB')

