import os
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from diffusers import AutoPipelineForInpainting
import torch.cuda
import random

'''Classe che eseguirà l'inpainting, generica, verrà specificato il diffuser sul costruct
in input si avranno tutti i necessari parametri per la pipe
in output l'immagine su cui è stato fatto l'inpaiting ed i suoi metadati'''


class Diffusable:

    def __init__(self, model, negative_prompt=None, prompt=None):
        self.model_path = model
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.pipe = AutoPipelineForInpainting.from_pretrained(self.model_path,
                                                              torch_dtype=torch.float16,
                                                              variant="fp16").to('cuda')

        self.avaible_seeds: list[int] = [x for x in range(5000)]  # metto 5000 seeds a disposizione
        self.image_toPipe: Image = None
        self.image_mask: Image = None
        self.inference_steps: int = None
        self.guidance_scale: float = None
        self.generator: torch.Generator = None
        self.inpainted: Image = None

    def generate_seed(self):
        return self.avaible_seeds.pop(random.randint(0, len(self.avaible_seeds)))

    def set_meta(self, inference_steps=35, guidance_scale=7.5):
        seed = self.generate_seed()
        self.generator = torch.Generator(device='cuda').manual_seed(seed)
        self.inference_steps = inference_steps
        self.guidance_scale = guidance_scale

        meta = PngInfo()
        meta.add_text('seed', str(seed))
        meta.add_text('prompt', self.prompt)
        meta.add_text('negative_prompt', self.negative_prompt)
        meta.add_text('inference_steps', str(inference_steps))
        meta.add_text('guidance_steps', str(guidance_scale))
        return meta

    def set_image_topipe(self, image: Image):
        self.image_toPipe = image

    def set_mask(self, image: Image):
        self.image_mask = image

    def do_inpaint(self):
        if self.generator:
            _image = self.pipe(prompt=self.prompt,
                               negative_prompt=self.negative_prompt,
                               image=self.image_toPipe,
                               mask_image=self.image_mask,
                               generator=self.generator,
                               height=self.image_toPipe.height,
                               width=self.image_toPipe.width,
                               num_inference_steps=self.inference_steps,
                               guidance_scale=self.guidance_scale).images[0]
        else:
            pass
