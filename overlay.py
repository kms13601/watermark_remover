import glob
import os
from func import *

path = '../test/data/'
png_paths = glob.glob(os.path.join(path, "*.png"))
jpg_paths = glob.glob(os.path.join(path, "*.jpg"))
jpeg_paths = glob.glob(os.path.join(path, "*.jpeg"))

img_paths = png_paths + jpg_paths + jpeg_paths
#img_paths = img_paths[585:]

#print(img_paths)

i=1
for img in img_paths :
    print(f"Processing {i}/{len(img_paths)}: {img}")
    # add_logo_randomly(img, '1')
    # add_logo_randomly(img, '2')
    # logo_crop(img, '3')
    # logo_crop(img, '4')
    add_logo_randomly(img, '5')
    logo_crop(img, '6')
    i+=1