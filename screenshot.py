import cv2
from mss import mss
from PIL import Image
import numpy as np
import time


frame = None
screen = mss()
monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}


def convert_rgb_to_bgr(img):
    return img[:, :, ::-1]


def take_screenshot():
    sct_img = screen.grab(monitor)
    img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    img = np.array(img)
    img = convert_rgb_to_bgr(img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_gray


def canny_image(img_grayscale, threshold=0.9):
    canny = cv2.Canny(img_grayscale, 25, 250)
    cv2.imwrite(str(time.time()) + '.png', canny)


canny_image(take_screenshot())

