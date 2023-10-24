import os
import sys
from datetime import datetime
import torch.cuda
from PIL import Image, ImageDraw, ImageFilter
from PIL.PngImagePlugin import PngInfo
from diffusers import AutoPipelineForInpainting
import random

SDV5_MODEL_PATH = os.getenv("SDV5_MODEL_PATH")
SDV5XL_INPAINT_MODEL_PATH = 'C:/Users/Alessandro/stable-diffusion-xl-1.0-inpainting-0.1/'
SAVE_PATH = os.path.join(os.environ['USERPROFILE'], "Desktop", "SDV5_OUTPUT/")
IMAGES_PATH = "C:/Users/Alessandro/Desktop/IMAGES/"





pipe = AutoPipelineForInpainting.from_pretrained(SDV5XL_INPAINT_MODEL_PATH, torch_dtype=torch.float16,
                                                 variant="fp16").to('cuda')

prompt: str = 'Florence city street photography, elegant, highly detailed, sharp details, ' \
              'realistic, italian architecture, clear sky' \
              'city center, ancient city, renaissance'
negative_prompt: str = 'Disfigured, cartoon, blurry'
inference_steps: int = 5
guidance_scale: float = 7.5
used_seed: list[int] = []

for file in os.listdir(IMAGES_PATH):
    # Load full image, must be 8-divisible
    print(f'Building {file}...')
    base_img = Image.open(IMAGES_PATH + file)

    '''
    # Adapt to my HW limitations, get a crop (why not resizing...?)
    b_w, b_h = base_img.size
    crop_xy = ((b_w - (b_w // 4)) // 2,
               (b_h - (b_h // 4)) // 2,
               (b_w + (b_w // 4)) // 2,
               (b_h + (b_h // 4)) // 2)
    crop_ToPipe = base_img.crop(crop_xy)
    '''
    # Resize to 2048Width
    aspect_ratio = base_img.height / base_img.width

    _ToPipe = base_img.resize((2048, int(2048*aspect_ratio)), Image.LANCZOS)
    # _ToPipe.show()

    # 512x512 square on Center mask, to_inpaint
    c_w, c_h = _ToPipe.size
    max_patch_size = 1024
    offset = ((c_w - max_patch_size) // 2, (c_h - max_patch_size) // 2,
              (c_w + max_patch_size) // 2, (c_h + max_patch_size) // 2)

    mask_img = Image.new(mode="RGB", size=_ToPipe.size, color='black')
    draw = ImageDraw.Draw(mask_img)
    draw.rectangle(offset, fill='white')
    # mask_img = mask_img.filter(ImageFilter.GaussianBlur(25))  # Better blending?

    # Generator for manual seed (?)
    seed: int = generate_seed()
    generator = torch.Generator(device='cuda').manual_seed(seed)

    synt_img = pipe(prompt=prompt, negative_prompt =negative_prompt,
                    image=_ToPipe, mask_image=mask_img,
                    generator=generator,
                    height=_ToPipe.height, width=_ToPipe.width,
                    num_inference_steps=inference_steps,
                    guidance_scale=guidance_scale).images[0]

    #base_img.paste(synt_img, crop_xy)

    # Saving png + writing some meta
    meta = PngInfo()
    meta.add_text('seed', str(seed))
    meta.add_text('prompt', prompt)
    meta.add_text('negative_prompt', negative_prompt)
    meta.add_text('inference_steps', str(inference_steps))
    meta.add_text('guidance_steps', str(guidance_scale))
    print(f'Saving {file}...\n')
    synt_img.save(SAVE_PATH + file.replace('.jpg', '') + '.png', pnginfo=meta)