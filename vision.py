import cv2
from mss import mss
from PIL import Image
import numpy as np
import time


class Vision:
    def __init__(self, window):
        self.assets = 'assets/img/'
        self.static_templates = {
            'amt_wood': self.asset('amt_wood'),
            'help': self.asset('help'),
            'res_field': self.asset('res_field'),
            'res_ore': self.asset('res_ore'),
            'res_wood': self.asset('res_wood'),
            'res_gold': self.asset('res_gold'),
            'res_rocks': self.asset('res_rocks'),
            'gather_gather': self.asset('gather_gather'),
            'army_status': self.asset('army_status'),
            'free_chest': self.asset('free_chest'),
            'free_chest_5x': self.asset('free_chest_5x'),
            'free_chest_claim': self.asset('free_chest_claim'),
            'free_speedup': self.asset('free_speedup'),
            'gather_auto_ass': self.asset('gather_auto_ass'),
            'gather_start': self.asset('gather_start'),
            'guild': self.asset('guild'),
            'kingdom': self.asset('kingdom'),
            'quest': self.asset('quest'),
            'quest_admin': self.asset('quest_admin'),
            'quest_collect': self.asset('quest_collect'),
            'quest_guild': self.asset('quest_guild'),
            'quest_has_completed': self.asset('quest_has_completed'),
            'quest_has_quests': self.asset('quest_has_quests'),
            'quest_start': self.asset('quest_start'),
            'quest_turf': self.asset('quest_turf'),
            'quest_vip': self.asset('quest_vip'),
            'quest_vip_lock': self.asset('quest_vip_lock'),
            'screen_close': self.asset('screen_close'),
            'screen_close_level_up': self.asset('screen_close_level_up'),
            'screen_close_main': self.asset('screen_close_main'),
            'turf': self.asset('turf'),
            'cr_none': self.asset('cr_none'),
            'cr_upgrade': self.asset('cr_upgrade'),
            'cr_no_research': self.asset('cr_no_research'),
            'cr_go': self.asset('cr_go'),
            'static_turf_statue': self.asset('static_turf_statue'),
            'expand_ongoing': self.asset('expand_ongoing')
        }
        self.templates = {k: cv2.imread(v, 0) for (k, v) in self.static_templates.items()}
        self.monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.screen = mss()
        self.frame = None
        self.window = window

    def asset(self, img):
        return self.assets + img + '.png'

    def convert_rgb_to_bgr(self, img):
        return img[:, :, ::-1]

    def take_screenshot(self):
        sct_img = self.screen.grab(self.monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return img_gray

    def refresh_frame(self):
        self.frame = self.take_screenshot()

    def match_template(self, img_grayscale, template, threshold=0.9):
        canny = cv2.Canny(img_grayscale, 25, 250)
        res = cv2.matchTemplate(canny, template, cv2.TM_CCOEFF_NORMED)
        # cv2.imwrite(str(time.time()) + '.png', canny)
        matches = np.where(res >= threshold)
        i = 0
        while i < len(matches[0]):
            if matches[1][i] < self.window.game['x1'] or matches[1][i] > self.window.game['x2'] or \
                    matches[0][i] < self.window.game['y1'] or matches[0][i] > self.window.game['y2']:
                matches = np.array([np.delete(matches[0], i), np.delete(matches[1], i)])
            else:
                i += 1
        return np.array([np.asarray(matches[0]), np.asarray(matches[1])])

    def find_template(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        return self.match_template(
            image,
            self.templates[name],
            threshold
        )

    def scaled_find_template(self, name, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        initial_template = self.templates[name]
        for scale in scales:
            scaled_template = cv2.resize(initial_template, (0, 0), fx=scale, fy=scale)
            matches = self.match_template(
                image,
                scaled_template,
                threshold
            )
            if np.shape(matches)[1] >= 1:
                return matches
        return matches

    def can_see_object(self, template, threshold=0.9):
        matches = self.find_template(template, threshold=threshold)
        return np.shape(matches)[1] >= 1

    def is_visible(self, asset, threshold=0.9):
        return self.can_see_object(asset, threshold)
