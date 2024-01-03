from PIL import Image
from PIL.PngImagePlugin import PngInfo
from diffusers import AutoPipelineForInpainting
import torch.cuda
import random

import Logging


class Diffusable:

    def __init__(self, model_path):
        torch.cuda.empty_cache()
        self.model = model_path
        self.hardware: str = ''
        self.pipe = None

        self.image_toPipe: Image = None
        self.image_mask: Image = None

        self.available_seeds: list[int] = [x for x in range(5000)]  # metto 5000 seeds a disposizione

        self.prompt: str = ''
        self.negative_prompt: str = ''
        self.inference_steps: int = None
        self.guidance_scale: float = None
        self.generator: torch.Generator = None

        self.logger = Logging.Logger()

    def set_model_hardware(self, hardware: str = None):
        self.hardware = hardware
        match hardware:
            case 'cuda':
                self.pipe = AutoPipelineForInpainting.from_pretrained(self.model,
                                                                      torch_dtype=torch.float16,
                                                                      variant="fp16").to('cuda')
            case 'cpu':
                self.pipe = AutoPipelineForInpainting.from_pretrained(self.model,
                                                                      variant="fp16").to('cpu')
            case _ :
                return None


    def tune_model(self, prompt=None, negative_prompt=None, inference_steps=35, guidance_scale=7.5):
        self.inference_steps = inference_steps
        self.guidance_scale = guidance_scale
        self.prompt = prompt
        self.negative_prompt = negative_prompt

    def generate_seed(self):
        return self.available_seeds.pop(random.randint(0, len(self.available_seeds)))

    def set_meta(self, mask):
        seed = self.generate_seed()
        self.generator = torch.Generator(device=self.hardware).manual_seed(seed)

        self.image_mask = mask

        meta = PngInfo()
        meta.add_text('seed', str(seed))
        meta.add_text('prompt', self.prompt)
        meta.add_text('negative_prompt', self.negative_prompt)
        meta.add_text('inference_steps', str(self.inference_steps))
        meta.add_text('guidance_steps', str(self.guidance_scale))
        return meta

    def set_image_topipe(self, image: Image):
        self.image_toPipe = image

    def __call__(self):
        try:
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
                return _image
            else:
                raise AttributeError
        except Exception as e:
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='ERROR',
                                    msg=f'Pipe: {e}')
