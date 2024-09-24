from PIL.PngImagePlugin import PngInfo
from PIL import Image, ImageChops
import random
import os
import shutil
import shutil as sh

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
"""
lines = []
with open('images_list_full.txt', 'rb') as file:
    lines = file.read().decode().split()

print(len(lines))

for line in lines.copy():
    if 'Flat' in line:
        lines.remove(line)

first_batch = random.sample(lines, 500)

for s in first_batch:
    lines.remove(s)
second_batch = random.sample(lines, 500)

for s in second_batch:
    lines.remove(s)

reals_batch = random.sample(lines, 1000)

for s in reals_batch:
    lines.remove(s)

prediction = random.sample(lines, 500)

with open('first_batch.txt', 'w') as file:
    for l in first_batch:
        file.write(l + '\n')

with open('second_batch.txt', 'w') as file:
    for l in second_batch:
        file.write(l + '\n')

with open('reals_batch.txt', 'w') as file:
    for l in reals_batch:
        file.write(l + '\n')

with open('prediction.txt', 'w') as file:
    for l in prediction:
        file.write(l + '\n')

#########################################
with open('prediction.txt', 'rb') as file:
    paths = file.read().decode().split()

random.shuffle(paths)

with open('images_list.txt', 'w') as file:
    tmp = random.sample(paths, 250)
    for l in tmp:
        paths.remove(l)
        file.write(l + '\n')

with open('to_copy.txt', 'w') as file:
    print(f'TO REALS: {len(paths)}')
    for l in paths:
        file.write(l + '\n')
"""

AI_destination = '/Prove/Cerro/TO_PREDICT/AI/'
REAL_destination = '/Prove/Cerro/TO_PREDICT/REALS/'

with open('to_copy.txt', 'rb') as file:
    paths = file.read().decode().split()

for p in paths:
    try:
        sh.copy2(p, REAL_destination)
        print(f'{os.path.basename(p)} COPIED')
    except Exception as e:
        print(f'NOT COPIED: {p}')

print(f'COPIED: {len(os.listdir(REAL_destination))} ORIGINAL IMAGES')

