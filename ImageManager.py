import os
import random
import Diffusable
import Logging
from PIL import Image, ImageDraw, ImageFilter
from PIL.PngImagePlugin import PngInfo


class ImageManager:

    def __init__(self, out_path: str, in_path: str = None):
        """
        Folder paths for retrieve given images
        """
        self.in_path: str = in_path
        self.out_path: str = out_path
        self.images_path: list[str] = list()

        """
        Used attributes to compute masks and generate Pipeline
        """
        self.mask_size: int = 2048
        self.n_masks: int = 10
        self.inpainted_images: list[Image] = list()

        self.logger = Logging.Logger()
        self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                tag='DEBUG',
                                msg=f'Input Path: {self.in_path}', msg2=f'Output Path: {self.out_path}')
        self.build_list()

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
            self.images_path = self.images_path[self.images_path.index(last_processed) + 1:]
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='DEBUG',
                                    msg=f'Last Processed retrieved: {last_processed}')
        except Exception as e:
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='ERROR',
                                    msg=str(e))
            self.list_images()

    def list_images(self):
        """
        List all available images and create a log file
        """
        with open('images_list.txt', 'w') as file:
            for _file in os.listdir(self.in_path):
                if self.is_image(os.path.join(self.in_path, _file)):
                    _inapp = os.path.join(self.in_path, _file)
                    self.images_path.append(_inapp)
                    file.write(_inapp + "\n")

        self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                tag='DEBUG',
                                msg='ImagesList Created!')

    def save_image(self, image: Image, mask: Image, tag, metadata: PngInfo = None):
        """
        Create a folder for each processed image, save each generated image + meta + relative mask
        """

        filename = os.path.normpath(image.filename)
        filename = filename.split(os.sep)[-1].replace('.jpg', '')

        if os.path.isdir(os.path.join(self.out_path, filename)):
            tmp_out = os.path.join(self.out_path, filename)
            filename = filename + '_' + tag
            image.save(os.path.join(tmp_out, filename + '.png'),
                       pnginfo=metadata)
            mask.save(os.path.join(tmp_out, filename + 'mask' + '.png'))
        else:
            os.mkdir(os.path.join(self.out_path, filename))
            self.save_image(image, mask, tag, metadata)

    def load_image(self):
        """
        Load the popped image from local list.
        Generate the required number of masks, using the given size for each.
        :return: PIL Image, filename: str, PIL Masks
        """
        filename = self.images_path.pop(0)
        im = Image.open(filename)
        """ONLY FOR DEBUG PURPOSES: RESIZE IMAGE"""
        aspect_ratio = im.height / im.width
        _ToPipe = im.resize((1024, int(1024 * aspect_ratio)), Image.LANCZOS)
        im = _ToPipe
        """END DEBUG"""
        masks = self.generate_masks(im)
        self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                tag='DEBUG',
                                msg=f'Loading Image & Building masks: {filename}')
        return im, masks

    def start_diffuse(self, model: str = 'SDV5', mask_size: int = 1024, n_masks: int = 1, prompt='', negative_prompt=''):
        try:
            diffuser = Diffusable.Diffusable(model, prompt=prompt, negative_prompt=negative_prompt)

            while self.images_path:
                self.mask_size = mask_size
                self.n_masks = n_masks

                _toInpaint, masks = self.load_image()
                diffuser.set_image_topipe(_toInpaint)
                filename = os.path.normpath(_toInpaint.filename)

                self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                        tag='DEBUG',
                                        msg=f'Processing: {filename.split(os.sep)[-1]}')

                for mask in masks:
                    diffuser.set_mask(mask)
                    meta = diffuser.set_meta(inference_steps=10, guidance_scale=8)
                    synth_image = diffuser.do_inpaint()  # CORE BUSINESS
                    self.save_image(synth_image, mask, str(masks.index(mask)), meta)

                Logging.log_image(filename)

            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='DEBUG',
                                    msg=f'List processing Ended')
        except Exception as e:
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='ERROR',
                                    msg=f'Exception: {str(e)}')

    def testingClass(self):
        while self.images_path:
            im, filename = self.load_image()
            # im.show()
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    msg=f'PROCESSING: {filename}')
            Logging.log_image(filename)

        self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                msg=f'List processing Ended!')

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
            top_left_offset = (0, 0, self.mask_size, self.mask_size)
            bottom_right_offset = (c_w - self.mask_size, c_h - self.mask_size,
                                   c_w + self.mask_size, c_h + self.mask_size)
            return [top_left_offset, center_offset, bottom_right_offset]

        def get_random_coordinates():
            x1 = random.randint(0, image.size[0])
            y1 = random.randint(0, image.size[1])
            x2 = random.randint(x1 + 1, image.size[0])
            y2 = random.randint(y1 + 1, image.size[1])
            if (x2 - x1) * (y2 - y1) >= 1024 * 1024:
                return [x1, y1, x2, y2]
            else:
                return get_random_coordinates()

        mask_batch: list[Image] = list()

        try:
            for offset in static_Sqare_masks():
                mask_batch.append(generate_mask(offset, image.size))

            if self.n_masks > 3:
                for i in range(self.n_masks - 3):
                    mask_batch.append(generate_mask(get_random_coordinates(), image.size))
        except Exception as e:
            self.logger.log_message(caller=self.__class__.__name__ + '.' + Logging.get_caller_name(),
                                    tag='ERROR',
                                    msg=f'Exception: {str(e)}')
        finally:
            return mask_batch
