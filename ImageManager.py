import os
import Logging
import Diffusable
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

    def __init__(self, in_path: str, out_path: str):
        self.in_path: str = in_path
        self.out_path: str = out_path
        self.images_path: list[str] = list()

        self.filename: str = ''
        self.mask_size: int = 1024

    def set_mask_size(self, size: int):
        self.mask_size = size

    def list_images(self):
        for file in os.listdir(self.in_path):
            if is_image(os.path.join(self.in_path, file)):
                self.images_path.append(os.path.join(self.in_path, file))

    # Save image with meta
    # TODO filename as previous + 'INPAINTED'
    def save_image(self, image: Image, metadata: dict):
        image.save(os.path.join(self.out_path, None))

    def load_image(self, path):
        im = Image.open(path)
        self.filename = im.filename[0: im.filename.index('.') - 1]
        return im

    def send_toPipe(self, model: str):
        # Generate 5 Masks
        # TODO logic for generating 5 masks
        mask_list: list[Image] = list()


        diffuse = Diffusable.Diffusable(model)

        inpainted_images: list[Image] = list()

        for mask in mask_list:
            diffuse.set_mask(mask)
            inpainted_images.append(diffuse.do_inpaint())

