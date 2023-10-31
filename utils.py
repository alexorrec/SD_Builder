import Logging
import ImageManager
import sys
import time


# TODO: implementare percorso di salvataggio con relativi dati
# TODO: rivedere la gestione delle eccezioni

SDV5XL_INPAINT_MODEL_PATH = 'C:/Users/Alessandro/stable-diffusion-xl-1.0-inpainting-0.1/'

log = Logging.Logger()
log.log_message(msg='MAIN TESTING')

_manager = ImageManager.ImageManager('C:\\Users\\Alessandro\\Desktop\\SDV5_OUTPUT',
                                     'C:\\Users\\Alessandro\\Desktop\\IMAGES')

_manager.start_diffuse(model=SDV5XL_INPAINT_MODEL_PATH,
                       mask_size=512,
                       n_masks=4,
                       prompt='Florence city view, reinassance, italy, rebuild what is in image',
                       negative_prompt='nude')

