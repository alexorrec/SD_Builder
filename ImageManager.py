import os
import Logging

from PIL import Image, ImageDraw, ImageFilter
from PIL.PngImagePlugin import PngInfo


def is_image(image_path):
    try:
        im = Image.open(image_path)
        im.verify()
        im.close()
        im = Image.open(image_path)
        im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        im.close()
        return True
    except:
        print(image_path, 'corrupted')
        return False


class ImageManager:

    def __init__(self, out_path: str, in_path: str = None):
        self.in_path: str = in_path
        self.out_path: str = out_path
        self.images_path: list[str] = list()

        self.mask_size: int = 1024
        self.logger = Logging.Logger()
        self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                msg=f'Input Path: {self.in_path}', msg2=f'Output Path: {self.out_path}')
        self.build_list()

    def build_list(self):
        try:
            with open('images_list.txt', 'rb') as file:
                self.images_path = file.read().decode().split()
            last_processed = self.logger.image_checkpoints
            self.images_path = self.images_path[self.images_path.index(last_processed) + 1:]
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    msg=f'Last Processed retrieved: {last_processed}')
        except Exception as e:
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(), msg=str(e))
            self.list_images()

    def list_images(self):
        with open('images_list.txt', 'a+') as file:
            for _file in os.listdir(self.in_path):
                if is_image(os.path.join(self.in_path, _file)):
                    _inapp = os.path.join(self.in_path, _file)
                    self.images_path.append(_inapp)
                    file.write(_inapp + "\n")
        self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                msg=f'ImagesList Created!')

    def set_mask_size(self, size: int):
        self.mask_size = size

    # Save image with meta
    # TODO filename as previous + 'INPAINTED'
    def save_image(self, image: Image, metadata: dict):
        image.save(os.path.join(self.out_path, None))

    def load_image(self):
        filename = self.images_path.pop(0)
        im = Image.open(filename)
        return im, filename

    def send_toPipe(self, model: str):
        # Generate 5 Masks
        # TODO logic for generating 5 masks
        mask_list: list[Image] = list()

        diffuse = Diffusable.Diffusable(model)

        inpainted_images: list[Image] = list()

        for mask in mask_list:
            diffuse.set_mask(mask)
            inpainted_images.append(diffuse.do_inpaint())

    def testingClass(self):
        while self.images_path:
            im, filename = self.load_image()
            # im.show()
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    msg=f'PROCESSING: {filename}')
            Logging.log_image(filename)
        self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                msg=f'List processing Ended!')
