import os
import string
import random
import Diffusable
import Logging
from PIL import Image, ImageDraw, ImageFilter
from PIL.PngImagePlugin import PngInfo

def check_path(path:str):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

class ImageManager:

    def __init__(self, out_path: str, in_path: str = None, folsize = False):
        """
        Folder paths for retrieve given images
        """
        self.in_path: str = in_path
        self.out_path: str = check_path(out_path)
        self.images_path: list[str] = list()
        """
        Image attributes
        """
        self._factor: int = 8
        self.mask_size: int = 1024
        self.n_masks: int = 5
        self.crop_offset = None
        self.full_image = None

        self.logger = Logging.Logger()
        self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                tag='DEBUG',
                                msg=f'Input Path: {self.in_path}', msg2=f'Output Path: {self.out_path}')
        """
        Start Building image list
        """
        self.build_list()

        """
        SET SIZES FOLDERS: ENABLE?
        """
        self._folsize = folsize
        self._sizes = set()

    def is_image(self, image_path):
        """
        Check wheterer the file is a valid Image
        """
        try:
            im = Image.open(image_path)
            im.verify()
            im.close()
            im = Image.open(image_path)
            im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            im.close()
            return True
        except Exception as e:
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='ERROR',
                                    msg=f'Corrupted: {image_path}', msg2=f'{str(e)}')
            return False

    def build_list(self):
        """
        For better debugging tracing, I'll keep a list of all images to be processed, and log them one by one
        In case of an interruption or an Unhandled Exception, the process starts back from the last processed image
        """
        try:
            with open('images_list.txt', 'rb') as file:
                self.images_path = file.read().decode().split()

            last_processed = self.logger.image_checkpoints

            """START REGION - EXCLUDE FLAT, RETRIEVE LAST PROCESSED PATH"""
            for _path in self.images_path:
                if 'Flat' in _path:
                    self.images_path.remove(_path)
                elif last_processed in _path:
                    last_processed = _path
            """END REGION"""
            self.images_path = self.images_path[self.images_path.index(last_processed) + 1:]
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='DEBUG',
                                    msg=f'Last Processed retrieved: {last_processed}')
        except Exception as e:
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='ERROR',
                                    msg=str(e))
            self.images_path.clear()
            self.list_images()

    def list_images(self, exist=False):
        """
        List all available images and create a log file
        """
        if not exist:
            with open('images_list.txt', 'w') as file:
                def DFS(path):
                    stack = []
                    ret = []
                    stack.append(path)
                    while len(stack) > 0:
                        tmp = stack.pop(len(stack) - 1)
                        if os.path.isdir(tmp):
                            ret.append(tmp)
                            for item in os.listdir(tmp):
                                stack.append(os.path.join(tmp, item))
                        elif self.is_image(tmp):
                            if 'Flat' not in tmp:
                                ret.append(tmp)
                                self.images_path.append(tmp)
                                file.write(tmp + "\n")

                DFS(self.in_path)


            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='DEBUG',
                                    msg='ImagesList Created!')
        else:
            with open('images_list.txt', 'rb') as file:
                self.images_path = file.read().decode().split()

    def set_attributes(self, _factor: int = 8, mask_size: int = 1024, n_masks=5):
        self.mask_size = mask_size
        self.n_masks = n_masks
        self._factor = _factor

    def save_image(self, filename: str, synth: Image, mask: Image, tag, metadata: PngInfo = None):
        """
        Create a folder for each processed image, save each generated image + meta + relative mask
        """
        if not self._folsize:
            if os.path.isdir(os.path.join(self.out_path, filename)):
                tmp_out = os.path.join(self.out_path, filename)
                filename = filename + '_' + tag
                try:
                    metadata.add_text('crop_area', '#'.join(str(x) for x in self.crop_offset)) # Later used for patch identification
                    Image.Image.paste(self.full_image, synth, self.crop_offset)  # Paste synth on original, with offset
                    self.full_image.save(os.path.join(tmp_out, filename + '.png'), pnginfo=metadata, format='png')

                    outer_mask = Image.new('RGB', self.full_image.size, 'black')
                    Image.Image.paste(outer_mask, mask, self.crop_offset)  # Paste synth on original respect to offset
                    outer_mask.save(os.path.join(tmp_out, filename + 'mask.png'), format='png')
                except Exception as e:
                    self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                            tag='DEBUG',
                                            msg=f'Error saving {filename}: {e}')
                    print(f'Error saving {filename}: {e}')
            else:
                os.mkdir(os.path.join(self.out_path, filename)) # Create folder and repeat!
                self.save_image(filename, synth, mask, tag, metadata)
        else:
            """SAME SIZES CROPS, UNDER SAME FOLDER - FOR DETECTION PURPOSES"""
            # No need to repaste cropped area in original image, save directly the cropped region
            # No need to save mask, just cropped image
            try:
                folder_name = str(synth.size).replace(' ', '').replace(',', 'x')
                if synth.size in self._sizes:
                    synth.save(os.path.join(self.out_path, os.path.join(folder_name, filename + tag + '.png')),
                               pnginfo=metadata, format='png')
                else:
                    os.mkdir(os.path.join(self.out_path, folder_name))
                    self._sizes.add(synth.size)
                    self.save_image(filename, synth, mask, tag, metadata)
            except Exception as ex:
                self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                        tag='DEBUG',
                                        msg=f'Error saving {filename}: {ex}')
                print(f'Error saving {filename}: {ex}')


    def ensure_divisible(self, n:int):
        if n % 8 == 0:
            return n
        else:
            while n % 8 != 0:
                n += 1
            return n


    def load_image(self):
        """
        Load the popped image from local list.
        Generate the required number of masks, using the given size for each.
        :return: PIL Image, filename: str, PIL Masks
        """
        self.full_image = None
        filename = self.images_path.pop(0)
        im = Image.open(filename).convert('RGB')

        crop_factor_w = self.ensure_divisible(int(im.width / 8 * self._factor))
        crop_factor_h = self.ensure_divisible(int(im.height / 8 * self._factor))

        self.crop_offset = ((im.width - crop_factor_w) // 2, (im.height - crop_factor_h) // 2,
                            (im.width + crop_factor_w) // 2, (im.height + crop_factor_h) // 2)

        self.full_image = im.copy()
        cropped = im.crop(self.crop_offset)

        masks = self.generate_masks(cropped)

        self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                tag='DEBUG',
                                msg=f'Loading Image & Building masks: {filename}')
        return cropped, filename, masks

    def get_filename(self, filename):
        try:
            filename = os.path.normpath(filename)
            filename = filename.split(os.sep)[-1].replace('.jpg', '')
        except Exception as e:
            filename = 'NEW_' + random.choices(string.ascii_lowercase)[0]
        finally:
            return filename

    def generate_masks(self, image: Image):
        """
        Generate a number of masks according to the specified quantity, 3 masks are given as default Square masks,
        more are randomly generated
        :param image:
        :return a list of masks:
        """

        def generate_mask(coordinates, size):
            mask = Image.new(mode="RGB", size=size, color='black')
            draw = ImageDraw.Draw(mask)
            draw.rectangle(coordinates, fill='white')
            return mask

        def static_Sqare_masks():
            c_w, c_h = image.size
            center_offset = ((c_w - self.mask_size) // 2, (c_h - self.mask_size) // 2,
                             (c_w + self.mask_size) // 2, (c_h + self.mask_size) // 2)
            top_left_offset = (300, 300, self.mask_size + 300, self.mask_size + 300)
            bottom_right_offset = (c_w - self.mask_size - 300, c_h - self.mask_size - 300,
                                   c_w - 300, c_h - 300)
            return [center_offset, top_left_offset, bottom_right_offset]

        def get_random_coordinates():
            x1 = random.randint(0, image.size[0])
            y1 = random.randint(0, image.size[1])
            x2 = random.randint(x1 + 1, image.size[0])
            y2 = random.randint(y1 + 1, image.size[1])
            if (x2 - x1) * (y2 - y1) >= self.mask_size * self.mask_size:
                return [x1, y1, x2, y2]
            else:
                return get_random_coordinates()

        mask_batch: list = list()

        try:
            for offset in static_Sqare_masks():
                mask_batch.append((generate_mask(offset, image.size), offset))

            if self.n_masks > 3:
                for i in range(self.n_masks - 3):
                    mask_batch.append(generate_mask(get_random_coordinates(), image.size))
        except Exception as e:
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='ERROR',
                                    msg=f'Exception: {str(e)}')
            print(e)
        finally:
            return mask_batch

    def __call__(self, diffuser: Diffusable):
        try:
            while self.images_path:
                _toInpaint, filepath, masks = self.load_image()

                diffuser.set_image_topipe(_toInpaint)

                filename = self.get_filename(filepath)
                self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                        tag='DEBUG',
                                        msg=f'Start Processing: {filename}')
                print(f'Start Processing: {filename}')

                for mask in masks:
                    meta = diffuser.set_meta(mask) #  and set mask

                    self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                            tag='DEBUG',
                                            msg=f'Start Processing: {filename}',
                                            msg2=f'Masks: {masks.index(mask)}')

                    synth_image = diffuser()  # CORE BUSINESS
                    self.save_image(filename, synth_image, mask[0], str(masks.index(mask)), meta)

                Logging.log_image(filename)

            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='DEBUG',
                                    msg=f'List processing Ended')
        except Exception as e:
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='ERROR',
                                    msg=f'Exception: {str(e)}')
            print(e)
