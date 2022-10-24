from cv2 import imread, Sobel, CV_32F, convertScaleAbs, addWeighted
from os import remove

def sobel(img_path):
    gray = imread(img_path, 0)
    ksize = 3
    gX = Sobel(gray, ddepth=CV_32F, dx=1, dy=0, ksize=ksize)
    gY = Sobel(gray, ddepth=CV_32F, dx=0, dy=1, ksize=ksize)
    gX = convertScaleAbs(gX)
    gY = convertScaleAbs(gY)
    combined = addWeighted(gX, 0.5, gY, 0.5, 0)
    return combined.mean()

def keep_best_image(image_paths):
    sobels = {}
    for image in image_paths:
        sobels[image] = sobel(image)
    max_sobel = sobels[max(sobels, key=sobels.get)]
    for image in image_paths:
        if sobels[image] != max_sobel:
            remove(image)