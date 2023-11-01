import os
import Logging
import ImageManager
import Diffusable
import sys
import time

# TODO: rivedere la gestione delle eccezioni
# TODO: idea - creare una classe che gestisca le maschere, e creare una maschera, con uno specifico prompt

SDV5XL_INPAINT_MODEL_PATH = 'C:/Users/Alessandro/stable-diffusion-xl-1.0-inpainting-0.1/'

log = Logging.Logger()
log.log_message(msg='MAIN TESTING')

_manager = ImageManager.ImageManager('C:\\Users\\Alessandro\\Desktop\\SDV5_OUTPUT',
                                     'C:\\Users\\Alessandro\\Desktop\\IMAGES')

_manager.set_attributes(resize_image=False,
                        mask_size=512,
                        n_masks=5)

diffuser = Diffusable.Diffusable(SDV5XL_INPAINT_MODEL_PATH)
diffuser.set_model_hardware('cpu')

diffuser.tune_model(prompt='Florence city view, reinassance, italy, detailed, 8k',
                    negative_prompt='nude',
                    inference_steps=35,
                    guidance_scale=7.5)

_manager(diffuser)

# os.system('shutdown -s -t 10')

