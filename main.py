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

    while not hardware == 'cuda' or hardware == 'cpu':
        hardware = input('Choosen Hardware: ')
    log.log_message(msg=f'Choosen Hardware: {hardware}')

    res_step = int(input('Resize step: '))

    _manager = ImageManager.ImageManager(out_path,
                                         in_path)

    _manager.set_attributes(resize_image=res_step,
                            mask_size=512,
                            n_masks=3)

    diffuser = Diffusable.Diffusable(model_path)
    diffuser.set_model_hardware(hardware)

    diffuser.tune_model(prompt='Florence city view, reinassance, italy, detailed, 8k, architecture, city of art, '
                               'snowy peaks mountain far in the background',
                        negative_prompt='nude, disfigured, cartoon',
                        inference_steps=35,
                        guidance_scale=7.5)

    _manager(diffuser)


if __name__ == '__main__':
    main()
    # os.system('shutdown -s -t 20')
