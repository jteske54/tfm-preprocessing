from cv2 import imread, imwrite, Sobel, CV_32F, convertScaleAbs, addWeighted
from pystackreg import StackReg
import numpy as np

def convert_greyscale(img: str):
    image = imread(img)
    r = np.max(image[:,:,0])
    g = np.max(image[:,:,1])
    b = np.max(image[:,:,2])
    if r != 0:
        image = image[:,:,0]
    elif g != 0:
        image = image[:,:,1]
    elif b != 0:
        image = image[:,:,2]
    else:
        pass
    imwrite(img, image)

def sobel(img_path):
    gray = imread(img_path, 0)
    ksize = 3
    gX = Sobel(gray, ddepth=CV_32F, dx=1, dy=0, ksize=ksize)
    gY = Sobel(gray, ddepth=CV_32F, dx=0, dy=1, ksize=ksize)
    gX = convertScaleAbs(gX)
    gY = convertScaleAbs(gY)
    combined = addWeighted(gX, 0.5, gY, 0.5, 0)
    return combined.mean()

def align_images(ref, mov, ph):
    ref_img = imread(ref,0)
    mov_img = imread(mov,0)
    ph_img = imread(ph,0)
    sr = StackReg(StackReg.TRANSLATION)
    sr.register(ref_img, mov_img)
    img_out = sr.transform(mov_img)
    ph_out = sr.transform(ph_img)
    imwrite(mov, img_out.astype('uint8'))
    imwrite(ph, ph_out.astype('uint8'))
    return 0