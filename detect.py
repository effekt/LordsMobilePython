import cv2
from mss import mss
from PIL import Image
import numpy as np
from window import Window
from matplotlib import pyplot as plt

window = Window()


frame = None
screen = mss()
monitor = {'top': 0, 'left': 0, 'width': window.game['w'], 'height': window.game['h']}


def convert_rgb_to_bgr(img):
    return img[:, :, ::-1]


def take_screenshot():
    sct_img = screen.grab(monitor)
    img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    img = np.array(img)
    img = convert_rgb_to_bgr(img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_gray


def match_template(img_grayscale, template, threshold=0.5):
    w, h = template.shape[::-1]
    ret, canny = cv2.threshold(img_grayscale, 150, 255, cv2.THRESH_BINARY)
    res = cv2.matchTemplate(canny, template, cv2.TM_CCOEFF_NORMED)
    matches = np.where(res >= threshold)
    print(matches)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(max_val)
    print(max_loc)
    bottom_right = (max_loc[0] + w, max_loc[1] + h)
    # cv2.rectangle(canny, max_loc, bottom_right, 0, 2)
    cv2.rectangle(canny, max_loc, bottom_right, 255, 2)
    cv2.imshow("Detection", canny)
    cv2.waitKey(0)
    # return np.array([np.asarray(matches[0]), np.asarray(matches[1])])


asset = cv2.imread('assets/img/etc/kingdom.jpg', 0)
match_template(take_screenshot(), asset, 0.85)
