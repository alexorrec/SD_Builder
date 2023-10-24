import os

from PIL import Image, ImageDraw, ImageFilter
from PIL.PngImagePlugin import PngInfo

'''GLOBAL'''
images_log = '.\\processed_images.txt'


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


def get_last_processed():
    with open(images_log, 'a+') as file:
        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        last_line = file.readline()
    return last_line


def write_underPipe(filename):
    with open(images_log, 'a+') as file:
        file.write(filename)


class ImageManager:

    def __init__(self, in_path: str, out_path: str):
        self.in_path: str = in_path
        self.out_path: str = out_path
        self.images_path: list[str] = list()

        self.last_processed: str = get_last_processed()  # un path però
        self.filename: str = ''
        self.mask_size: int = 1024

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

    def set_mask_size(self, size):
        self.mask_size = size

    def send_toPipe(self):
        pass
