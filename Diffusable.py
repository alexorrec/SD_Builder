import os
from PIL import Image
from diffusers import AutoPipelineForInpainting
import torch.cuda

'''Classe che eseguirà l'inpainting, generica, verrà specificato il diffuser sul costruct
in input si avranno tutti i necessari parametri per la pipe
in output l'immagine su cui è stato fatto l'inpaiting ed i suoi metadati'''


class Diffusable:

    def __init__(self, model, negative_prompt=None, prompt=None):
        assert model
        self.model_path = model
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.pipe = AutoPipelineForInpainting.from_pretrained(self.model_path, torch_dtype=torch.float16,
                                                              variant="fp16").to('cuda')

        self.image_toPipe: Image = None
        self.image_mask: Image = None
        self.inference_steps: int = 35
        self.guidance_scale: float = 7.5
        self.generator: torch.Generator = None
        self.inpainted: Image

    def set_inference_step(self, steps: int):
        self.inference_steps = steps

    def set_guidance_scale(self, scale: float):
        self.guidance_scale = scale

    def set_generator_seed(self, seed: int):
        self.generator = torch.Generator(device='cuda').manual_seed(seed)

    def set_image(self, image: Image):
        self.image_toPipe = image

    def set_mask(self, image: Image):
        self.image_toPipe = image

    def do_inpaint(self):
        return self.pipe(prompt=self.prompt, negative_prompt=self.negative_prompt,
                         image=self.image_toPipe, mask_image=self.image_mask,
                         generator=self.generator,
                         height=self.image_toPipe.height, width=self.image_toPipe.width,
                         num_inference_steps=self.inference_steps,
                         guidance_scale=self.guidance_scale).images[0]
