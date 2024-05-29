from PIL.PngImagePlugin import PngInfo
from PIL import Image, ImageChops
import random
import os
import shutil


"""
image = Image.open('DJI_0499-TESTING.jpg')
print(f"Original image size: {image.size}\n")
# _factor = int(input('Bounded Box Factor (1 - 8): '))
#c_w, c_h = image.size

r = [8]
for i in r:
    _factor = i

    crop_factor_w = int(image.width / 8 * _factor)
    crop_factor_h = int(image.height / 8 * _factor)

    crop_offset = ((image.width - crop_factor_w) // 2, (image.height - crop_factor_h) // 2,
                   (image.width + crop_factor_w) // 2, (image.height + crop_factor_h) // 2)

    print(f"_factor: {_factor}")
    print(f"crop offset: {crop_offset}")

    cropped = image.crop(crop_offset)
    print(f'CROPPED IMAGE SIZE: {cropped.size}')
    print()

    inverted_image = ImageOps.invert(cropped)
    #inverted_image.show()
    Image.Image.paste(image, inverted_image, crop_offset)
    image.show()



img_list = 'images_list.txt'
processed_img = 'processed_images.txt'



with open('images_list.txt', 'rb') as file:
    images_path = file.read().decode().split()

with open('processed_images.txt', 'rb') as file:
    last_processed = file.read().decode().split()[-1]
print(last_processed)

for _path in images_path:
    if 'Flat' in _path:
        images_path.remove(_path)
    elif last_processed in _path:
        last_processed = _path
        break

print(last_processed)

def copy_images(imgs, out_folder):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    for image_path in imgs:

        filename = os.path.basename(image_path)

        destination_path = os.path.join(out_folder, filename)

        shutil.copy2(image_path, destination_path)
        print(f"Image '{filename}' copied to '{out_folder}'")

with open('images_list.txt', 'rb') as file:
    images = file.read().decode().split()

out = '/Prove/Cerro/REALS'

copy_images(images, out)


im = Image.open('D02_L4S2C2.jpeg_0.png')
mask = Image.open('D02_L4S2C2.jpeg_0mask.png')


bbox = mask.getbbox()


cropped = im.crop(bbox)
cropped.show('cropped')
"""