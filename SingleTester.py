import os

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from diffusers import AutoPipelineForInpainting
from diffusers.utils import load_image
import torch.cuda
import random



