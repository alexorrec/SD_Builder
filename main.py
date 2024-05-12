import os
import Logging
import ImageManager
import Diffusable


def main(model_path: str = None, in_path: str = None, out_path: str = None, hardware: str = None):
    log = Logging.Logger()
    log.log_message(msg='STARTING PROCESS')

    while not model_path:
        if os.getenv("SDV5XL") and not model_path:
            model_path = os.getenv("SDV5XL")
        else:
            model_path = input("Path to model: ")

    log.log_message(msg=f'Choosen model: {model_path}')

    while not in_path:
        in_path = input('Input Path: ')
    log.log_message(msg=f'Input Path: {in_path}')

    while not out_path:
        out_path = input('Output Path: ')
    log.log_message(msg=f'Output Path: {out_path}')

    """
    while 'cuda' not in hardware  or 'cpu' not in hardware:
        hardware = input('Choosen Hardware: ')
    """
    log.log_message(msg=f'Choosen Hardware: {hardware}')

    crop_step = int(input('Crop step: '))

    _manager = ImageManager.ImageManager(out_path,
                                         in_path,
                                         folsize=False) # TESTING 27/04/24

    _manager.set_attributes(_factor=crop_step,
                            mask_size=512,
                            n_masks=1)

    diffuser = Diffusable.Diffusable(model_path)
    diffuser.set_model_hardware(hardware)

    """
    Actual used prompt:
    Florence city view, reinassance, italy, 8k, architecture, city of art, 
    italian architecture, realistic landscape photography, realistic colours, sharp details
    """
    diffuser.tune_model(prompt='Florence city view, reinassance, italy, architecture, city of art, '
                               'italian architecture, realistic city photography, realistic colours, sharp details, photorealistic',
                        negative_prompt='nude, disfigured, cartoon',
                        inference_steps=35,
                        guidance_scale=7.5)

    _manager(diffuser)


if __name__ == '__main__':
    main(
        model_path='/Prove/Cerro/models/stable-diffusion-xl-1.0-inpainting-0.1',
        in_path='/images/images/forensic_datasets/Container_Datasets/FloreView/Dataset',
        out_path='/Prove/Cerro/OUT_XL',
        hardware='cuda:1'
    )
    # os.system('shutdown -s -t 20')
