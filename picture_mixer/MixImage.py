import cv2 as cv
from style_transfer.learn import StyleTransfer
from PIL import Image
import numpy as np


def zoom_image(src, zoom):
    deltaY = int((src.shape[0] - src.shape[0] / zoom) / 2)
    deltaX = int((src.shape[0] - src.shape[0] / zoom) / 2)
    return src[deltaY : src.shape[0] - deltaY, deltaX: src.shape[1] - deltaX]


def mix_images(image1_path: str, image2_path: str):
    image1 = cv.imread(image1_path)
    image2 = cv.imread(image2_path)
    image2 = zoom_image(image2, 1.1)
    image1 = zoom_image(image1, 1.1)
    styleImage = cv.resize(image2, (image1.shape[1], image1.shape[0]))
    image1 = cv.cvtColor(image1, cv.COLOR_RGB2GRAY)
    image2 = cv.cvtColor(styleImage, cv.COLOR_RGB2GRAY)
    image1_thresh = cv.adaptiveThreshold(image1, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
    image2_thresh = cv.adaptiveThreshold(image2, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
    merged_image = cv.bitwise_and(image1_thresh, image2_thresh)
    merged_image = cv.dilate(merged_image, (3, 3), iterations=1)
    # merged_image = cv.erode(merged_image, (3, 3), iterations=1)
    merged_image = cv.medianBlur(merged_image, 3)
    merged_image = cv.cvtColor(merged_image, cv.COLOR_GRAY2RGB)
    cv.imwrite("temp/main.jpg", merged_image)
    cv.imwrite("temp/style.jpg", styleImage)
    transfer = StyleTransfer()
    artwork = transfer(Image.fromarray(merged_image), Image.fromarray(styleImage), iter=100, area=707)
    # b, g, r = artwork.split()
    # artwork = Image.merge("RGB", (r, g, b))
    # artwork.save("temp/result.jpg")
    opencv_image = np.array(artwork)
    cv.imwrite("temp/result.jpg", opencv_image)
    return opencv_image
    # return merged_image

