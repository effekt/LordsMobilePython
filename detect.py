import cv2
from mss import mss
from PIL import Image
import numpy as np
from window import Window

window = Window()


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


def match_template(img_grayscale, template, threshold=0.5):
    canny = cv2.Canny(img_grayscale, 25, 250)
    res = cv2.matchTemplate(canny, template, cv2.TM_CCOEFF_NORMED)
    matches = np.where(res >= threshold)
    i = 0
    while i < len(matches[0]):
        if matches[1][i] < window.game['x1'] or matches[1][i] > window.game['x2'] or \
                matches[0][i] < window.game['y1'] or matches[0][i] > window.game['y2']:
            matches = np.array([np.delete(matches[0], i), np.delete(matches[1], i)])
        else:
            i += 1
    print(matches)
    return np.array([np.asarray(matches[0]), np.asarray(matches[1])])


asset = cv2.imread('assets/img/static_turf_statue.png', 0)
match_template(take_screenshot(), asset, 0.2)

# asset = cv2.imread('assets/img/res_field_1.png', 0) threshold = 0.45
# asset = cv2.imread('assets/img/turf.png', 0) thr = 0.9
# asset = cv2.imread('assets/img/res_ore.png', 0) thresh = 0.45
# asset = cv2.imread('assets/img/res_rocks.png', 0) thresh = 0.45
# asset = cv2.imread('assets/img/screen_close.png', 0) thresh = 0.5
# asset = cv2.imread('assets/img/res_wood.png', 0) thresh = 0.6
# asset = cv2.imread('assets/img/res_gold.png', 0) thresh = 0.5
# asset = cv2.imread('assets/img/help.png', 0) thresh = 0.8
# asset = cv2.imread('assets/img/quest_collect.png', 0) thresh = 0.4
