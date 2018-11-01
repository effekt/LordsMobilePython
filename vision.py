import cv2
from mss import mss
from PIL import Image
import numpy as np
import time


class Vision:
    def __init__(self, window):
        self.assets = 'assets/img/'
        self.static_templates = {
            'chest_collect': self.asset('chest/collect'),
            'chest_5x': self.asset('chest/5x'),
            'chest_window': self.asset('chest/window'),
            'etc_close': self.asset('etc/close'),
            'dev_build': self.asset('dev/build'),
            'dev_help': self.asset('dev/help'),
            'dev_free': self.asset('dev/free'),
            'dev_no_cr': self.asset('dev/no_cr'),
            'dev_upgrade': self.asset('dev/upgrade'),
            'dev_go': self.asset('dev/go'),
            'dev_new': self.asset('dev/new'),
            'etc_turf': self.asset('etc/turf'),
            'etc_kingdom': self.asset('etc/kingdom'),
            'guild_open': self.asset('guild/open'),
            'hud_army': self.asset('hud/army'),
            'hud_gift': self.asset('hud/gift'),
            'quest_admin_comp': self.asset('quest/admin_comp'),
            'quest_collect': self.asset('quest/collect'),
            'quest_guild_comp': self.asset('quest/guild_comp'),
            'quest_has_completed': self.asset('quest/has_completed'),
            'quest_has_q': self.asset('quest/has_quests'),
            'quest_start': self.asset('quest/start'),
            'quest_turf_comp': self.asset('quest/turf_comp'),
            'quest_vip_chest': self.asset('quest/vip_chest'),
            'quest_vip_claim': self.asset('quest/vip_claim'),
            'quest_vip_comp': self.asset('quest/vip_comp'),
            'quest_window': self.asset('quest/window'),
            'res_field': self.asset('res/field'),
            'res_gold': self.asset('res/gold'),
            'res_gold2': self.asset('res/gold2'),
            'res_ore': self.asset('res/ore'),
            'res_ore2': self.asset('res/ore2'),
            'res_rocks': self.asset('res/rocks'),
            'res_woods': self.asset('res/woods'),
            'res_woods2': self.asset('res/woods2'),
            'res_txt_f': self.asset('res/txt_field'),
            'res_txt_g': self.asset('res/txt_gold'),
            'res_txt_o': self.asset('res/txt_ore'),
            'res_txt_r': self.asset('res/txt_rocks'),
            'res_txt_w': self.asset('res/txt_woods'),
            'res_gather': self.asset('res/gather'),
            'turf_barracks': self.asset('turf/barracks'),
            'turf_infirmary': self.asset('turf/infirmary'),
            'turf_shelter': self.asset('turf/shelter'),
            'turf_statue': self.asset('turf/statue')
        }
        self.templates = {k: cv2.imread(v, 0) for (k, v) in self.static_templates.items()}
        self.monitor = {'top': 0, 'left': 0, 'width': window.game['w'], 'height': window.game['h']}
        self.screen = mss()
        self.frame = None
        self.window = window

    def asset(self, img):
        return self.assets + img + '.JPG'

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

    def match_template(self, img_grayscale, template, threshold=0.9, max_v=False):
        ret, canny = cv2.threshold(img_grayscale, 150, 255, cv2.THRESH_BINARY)
        res = cv2.matchTemplate(canny, template, cv2.TM_CCOEFF_NORMED)
        if not max_v:
            matches = np.where(res >= threshold)
        else:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            matches = ([max_loc[1]], [max_loc[0]])
        return np.array([np.asarray(matches[0]), np.asarray(matches[1])])

    def find_template(self, name, image=None, threshold=0.9, max_v=False):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        return self.match_template(
            image,
            self.templates[name],
            threshold,
            max_v
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
