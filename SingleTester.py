import os

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from diffusers import AutoPipelineForInpainting
from diffusers.utils import load_image
import torch.cuda
import random

image = Image.open('D01_L1S4C3.png')
c_w, c_h = image.size
center_offset = ((c_w - 2048) // 2, (c_h - 2048) // 2,
                 (c_w + 2048) // 2, (c_h + 2048) // 2)
cropped = image.crop(center_offset)


#im2.show()

im2 = Image.open('D01_L1S5C3.png')

Image.Image.paste(im2, cropped, center_offset)
im2.show()
#img.show()



